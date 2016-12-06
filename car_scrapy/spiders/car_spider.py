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


class CarSpider(Spider):
    """Base class for spiders"""
    name = "car-spider"
    start_urls = ["http://www.caranddriver.com/api/vehicles/models-by-make/18/json?ddIgnore=1",
                  "http://www.caranddriver.com/api/vehicles/models-by-make/19/json?ddIgnore=1",]

    def parse(self, response):
        """Default function to receive response object from start_urls request"""

        json_response = json.loads(response.body_as_unicode())
        orig_item = CarScrapyItem()

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

        photos_url_xpath = '//div[@id="overview--primary-submodel"]/div[2]/div[1]/a/@href'
        photos_url_extract = sel.xpath(photos_url_xpath).extract()[0]
        re_photos_url = re.compile('http://www\\.caranddriver\\.com/photo-gallery/([\\-\\S/]+)')
        if re_photos_url.match(photos_url_extract):
            item['photos_url'] = photos_url_extract

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
            yield item_trim
