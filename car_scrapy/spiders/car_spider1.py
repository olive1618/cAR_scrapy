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
    name = "new-car-spider"
    start_urls = ["http://www.caranddriver.com/api/vehicles/models-by-make/18/json?ddIgnore=1",]

    def parse(self, response):
        """Default function to receive response object from start_urls request"""

        json_response = json.loads(response.body_as_unicode())
        orig_item = CarScrapyItem()

        orig_item['make'] = json_response['vehicles']['make']['name']
        orig_item['make_id'] = json_response['vehicles']['make']['id']
        orig_item['make_url_alias'] = json_response['vehicles']['make']['url_alias']

        num_models = json_response['vehicles']['counts']['models']
        models = []
        for i in range(num_models):
            model = json_response['vehicles']['models'][i]['name']
            model_id = json_response['vehicles']['models'][i]['id']
            model_url_alias = json_response['vehicles']['models'][i]['url_alias']
            models.append((model, model_id, model_url_alias))

        for this_model in models:
            item = copy.deepcopy(orig_item)
            item["model"] = this_model[0]
            item["model_id"] = this_model[1]
            item["model_url_alias"] = this_model[2]

            model_url = 'http://www.caranddriver.com/{}/{}'
            model_url = model_url.format(item['make_url_alias'], item['model_url_alias'])
            request = Request(model_url, callback=self.load_model, meta={'item':item})
            yield request


    def load_model(self, response):
        """Add the photo gallary URL to the item"""
        item = response.meta['item']
        sel = Selector(response)

        photos_url_xpath = '//div[@id="overview--primary-submodel"]/div[2]/div[1]/a/@href'
        photos_url_response = sel.xpath(photos_url_xpath).extract()[0]
        re_photos_url = re.compile('http://www\\.caranddriver\\.com/photo-gallery/([\\-\\S/]+)')
        if re_photos_url.match(photos_url_response):
            item['photos_url'] = photos_url_response

        model_url = 'http://www.caranddriver.com/api/vehicles/styles-by-model/{}/json?ddIgnore=1'
        callstack = [
            {'url': model_url.format(item['model_id']), 'callback': self.load_style}
        ]
        item['callstack'] = callstack

        return self.callnext(response)


    def callnext(self, response):
        """Avoid callback hell of chaining callbacks.  Use callstack."""
        # Get the meta object from the request, as the response does not contain it.
        meta = response.request.meta
        item = meta['item']

        # Items remaining in the stack? Execute them
        if len(item['callstack']) > 0:
            tgt = item['callstack'].pop(0)
            yield Request(tgt['url'], meta=meta, callback=tgt['callback'], errback=self.callnext)
        else:
            item.pop('callstack', None)
            yield item


    def load_style(self, response):
        """Get style info"""
        item = response.meta['item']
        json_response = json.loads(response.body_as_unicode())

        num_styles = len(json_response['vehicles']['styles']['groups'])
        styles = []
        for i in range(num_styles):
            style = json_response['vehicles']['styles']['groups'][i]['groupname']
            style_id = json_response['vehicles']['styles']['groups'][i]['submodel_group_id']
            styles.append((style, style_id))

        for this_style in styles:
            item1 = copy.deepcopy(item)
            item1["style"] = this_style[0]
            item1["style_id"] = this_style[1]
            return self.callnext(response)
