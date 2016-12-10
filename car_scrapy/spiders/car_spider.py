"""
Instructions to spider for how to find exact data.
Scapy uses xpath selector patterns to find the desired elements to scrape.
"""
import re
import copy
import json
from scrapy.selector import Selector
from scrapy import Spider
from scrapy.http import Request
from car_scrapy.items import CarScrapyItem
from car_scrapy.makes import ALL_MAKES_URLS


class CarSpider(Spider):
    """Base class for spiders"""
    name = "car-spider"
    start_urls = ALL_MAKES_URLS

    def parse(self, response):
        """Default function to receive response object from start_urls request"""

        json_response = json.loads(response.body_as_unicode())
        orig_item = CarScrapyItem()

        orig_item['processed'] = False
        orig_item['make'] = json_response['vehicles']['make']['name']
        orig_item['make_id'] = json_response['vehicles']['make']['id']
        orig_item['make_url_alias'] = json_response['vehicles']['make']['url_alias']

        num_models = len(json_response['vehicles']['models'])
        for i in range(num_models):
            item = copy.deepcopy(orig_item)
            item["model"] = json_response['vehicles']['models'][i]['name']
            item["model_id"] = json_response['vehicles']['models'][i]['id']
            item["model_url_alias"] = json_response['vehicles']['models'][i]['url_alias']

            model_url = 'http://www.caranddriver.com/{}/{}'
            model_url = model_url.format(item['make_url_alias'], item['model_url_alias'])
            request = Request(url=model_url, callback=self.load_model, meta={'item':item})
            yield request


    def load_model(self, response):
        """Add the photo gallary URL to the item if extracted href matches regex"""
        item = response.meta['item']
        sel = Selector(response)

        # URL for the user facing page with the image carousel
        photos_url_xpath = '//div[@id="overview--primary-submodel"]/div[2]/div[1]/a/@href'
        photos_url_extract = sel.xpath(photos_url_xpath).extract()[0]
        re_photos_url = re.compile('http://www\\.caranddriver\\.com/photo-gallery/([\\-\\S/]+)')
        if re_photos_url.match(photos_url_extract):
            item['imgs_home_url'] = photos_url_extract

            # URL for the AngularJS callback with the indivual img URLs nested
            # Get this make/model's tagline that goes in the AngularJS callback
            tagline = photos_url_extract.split('gallery/')[-1]
            ng_callback = 'http://blog.caranddriver.com/wp-json/posts?_jsonp=angular.callbacks'
            ng_callback += '._0&filter%5Bname%5D={}&filter%5Bposts_per_page%5D=1&type=gallery'
            item['imgs_ng_callback'] = ng_callback.format(tagline)

        style_url = 'http://www.caranddriver.com/api/vehicles/styles-by-model/{}/json?ddIgnore=1'
        style_url = style_url.format(item['model_id'])
        request = Request(url=style_url, callback=self.load_style, meta={'item':item})
        yield request


    def load_style(self, response):
        """Get style info"""
        item = response.meta['item']
        json_response = json.loads(response.body_as_unicode())

        num_styles = len(json_response['vehicles']['styles']['groups'])
        for i in range(num_styles):
            item_style = copy.deepcopy(item)
            this_style = json_response['vehicles']['styles']['groups'][i]
            item_style["style"] = this_style['groupname']
            item_style["style_id"] = this_style['submodel_group_id']
            item_style['first'] = False
            if i == 0:
                item_style['first'] = True

            trim_url = 'http://www.caranddriver.com/api/payments/trims-by-sub'
            trim_url += 'model-group/{}/{}/json?ddIgnore=1'
            trim_url = trim_url.format(item_style['model_id'], item_style['style_id'])
            request = Request(url=trim_url, callback=self.load_trim, meta={'item':item_style})
            yield request


    def load_trim(self, response):
        """Get trim info"""
        item = response.meta['item']
        json_response = json.loads(response.body_as_unicode())

        num_trims = len(json_response['alltrims'])
        for i in range(num_trims):
            item_trim = copy.deepcopy(item)
            item_trim["trim"] = json_response['alltrims'][i]["friendly_name"]
            item_trim["trim_id"] = json_response['alltrims'][i]["id"]
            item_trim["year"] = json_response['alltrims'][i]["year"]
            item_trim["msrp"] = json_response['alltrims'][i]["base_msrp"]
            chrome_data = json_response['alltrims'][i]['chrome_data']
            item_trim["num_passengers"] = chrome_data["Passenger Capacity"]["value"]
            item_trim['mpg_city'] = chrome_data["EPA Fuel Economy Est - City"]["value"]
            item_trim['mpg_hwy'] = chrome_data["EPA Fuel Economy Est - Hwy"]["value"]
            item_trim["drivetrain"] = chrome_data["Drivetrain"]["value"]
            item_trim["engine_type"] = chrome_data["Engine Type"]["value"]
            item_trim["hp_at_rpm"] = chrome_data["SAE Net Horsepower @ RPM"]["value"]
            item_trim["transmission"] = chrome_data["Trans Type"]["value"]

            # If this is the first style/trim combo, make additional Request
            #  to the angular callback to get the individual image URLs
            if i == 0 and item_trim['first'] is True and 'imgs_ng_callback' in item_trim:
                request = Request(url=item_trim['imgs_ng_callback'], callback=self.load_indv_imgs,
                                  meta={'item':item_trim})
                yield request
            item_trim.pop('first', None)
            yield item_trim

    def load_indv_imgs(self, response):
        """Add individual image URLs to the first style/trim document"""
        item = response.meta['item']
        jsonp = response.body
        jsons = str(jsonp, 'utf-8') #Bytes object to string
        jsons = jsons[jsons.index("(") + 2 : jsons.rindex(")") - 1] #Trim the callback wrapping
        norm_json = json.loads(jsons)

        indv_img_list = []
        for img_obj in norm_json['slides']: # Slides is an array of dicts
            img_set = img_obj['images'] # Url dict within given img dict
            different_img_sizes = {}
            for k in img_set.keys():
                if str(img_set[k]) == img_set[k]:
                    different_img_sizes[k] = img_set[k]
                else:
                    url_idx = [idx for idx, val in enumerate(img_set[k]) if "http" in str(val)][0]
                    different_img_sizes[k] = img_set[k][url_idx]
            indv_img_list.append(different_img_sizes)
        # Once all individual img URLs are processed, update key in doc with list
        item['imgs_indv_url'] = indv_img_list
        yield item
