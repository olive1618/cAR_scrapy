from scrapy.selector import Selector
from scrapy import Spider
from scrapy.http import Request
from car_scrapy.items import TestItem


class CarSpider(Spider):
    """Base class for spiders"""
    name = "test-spider"
    start_urls = ["http://www.caranddriver.com",]

    def parse(self, response):
        sel = Selector(response)
        item = TestItem()

        request = Request(response.url, callback=self.load_first, meta={'item':item})
        yield request


    def callnext(self, response):
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

    def load_first(self, response):
        item = response.meta['item']
        sel = Selector(response)

        test_xpath = '//div[@id="vehicle-research"]/header/text()'
        test_response = sel.xpath(test_xpath).extract()[0]
        item['title'] = test_response

        callstack = [
            {'url': 'http://www.caranddriver.com/best-sedans', 'callback': self.load_second},
            {'url': 'http://www.caranddriver.com/mazda/mazda-3', 'callback': self.load_third}
        ]
        item['callstack'] = callstack

        return self.callnext(response)


    def load_second(self, response):
        item = response.meta['item']
        sel = Selector(response)

        test_xpath = '//div[@id="content"]/h1/text()'
        test_response = sel.xpath(test_xpath).extract()[0]
        item['sedans'] = test_response

        return self.callnext(response)


    def load_third(self, response):
        item = response.meta['item']
        sel = Selector(response)

        test_xpath = '//div[@id="overview--primary-submodel"]/h1/text()'
        test_response = sel.xpath(test_xpath).extract()[0]
        item['mazda'] = test_response

        return self.callnext(response)
