"""
Instructions to spider for how to find exact data.
Scapy uses xpath selector patterns to find the desired elements to scrape.
"""
import re
import json
from scrapy.selector import Selector
from scrapy import Spider
from scrapy.http import Request
from car_scrapy.items import CarScrapyItem


class CarSpider(Spider):
    """Base class for spiders"""
    name = "car-spider"
    start_urls = ["http://www.caranddriver.com/volkswagen/golf-r",]

    def parse(self, response):
        """Parse the make, model, and photos url for a given make/model"""
        sel = Selector(response)
        item = CarScrapyItem()

        # Photos url to be used later to scrape images. Match to regex.
        photos_url_xpath = '//div[@id="overview--primary-submodel"]/div[2]/div[1]/a/@href'
        photos_url_response = sel.xpath(photos_url_xpath).extract()[0]
        re_photos_url = re.compile('http://www\\.caranddriver\\.com/photo-gallery/([\\-\\S/]+)')
        if not re_photos_url.match(photos_url_response):
            item['photos_url'] = photos_url_response

        # Get make name and model ID from xpath response
        make_model_xpath = '//div[@id="content"]/script/text()'
        make_model_response = sel.xpath(make_model_xpath).extract()[0]
        make = re.findall(r'\"(.+?)\"', make_model_response)[1]
        item['make'] = make
        model_id = re.findall(r'\"(.+?)\"', make_model_response)[0]
        item['model_id'] = model_id
        model_url = "http://www.caranddriver.com/api/vehicles/styles-by-model/{}/json?ddIgnore=1"
        model_url = model_url.format(model_id)
        request = Request(model_url, callback=self.parse_style)
        request.meta['style_trim_obj'] = {}
        request.meta['item'] = item
        yield request

    def parse_style(self, response):
        """Object's keys are tuples of each style's ID, name, and year"""
        obj = response.meta['style_trim_obj']
        item = response.meta['item']
        model_id = item['model_id']
        json_response = json.loads(response.body_as_unicode())
        num_styles = len(json_response['vehicles']['styles']['groups'])

        for i in range(num_styles):
            style_id = json_response['vehicles']['styles']['groups'][i]["submodel_group_id"]
            style_name = json_response['vehicles']['styles']['groups'][i]["groupname"]
            style_year = json_response['vehicles']['styles']['groups'][i]["default_submodel_year"]
            obj[(style_id, style_name, style_year)] = {}
            trim_url = 'http://www.caranddriver.com/api/payments/trims-by-submodel-group'
            trim_url += '/{}/{}/json?ddIgnore=1'
            trim_url = trim_url.format(model_id, style_id)
            request = Request(trim_url, callback=self.parse_trim)
            request.meta['style_trim_obj'] = obj
            yield request

    def parse_trim(self, response):
        """Add trim sub-object to each style object"""
        obj = response.meta['style_trim_obj']
        all_styles = obj.keys()
        json_response = json.loads(response.body_as_unicode())
        num_trims = len(json_response["alltrims"])
        for i in range(num_trims):
            trim_id = json_response["alltrims"][i]["submodel_id"]
            trim_msrp = json_response["alltrims"][i]["base_msrp"]
            style_id = json_response["alltrims"][i]["submodel_group_id"]
            for style in all_styles:
                if style[0] == style_id:
                    obj[style][trim_id] = [trim_msrp]
        yield obj
