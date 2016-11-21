"""Instructions to spider for how to find exact data"""

from scrapy.selector import Selector
from scrapy import Spider
from car_scrapy.items import CarScrapyItem


class CarSpider(Spider):
    """Base class for spiders"""
    name = "car-spider"
    allowed_domains = ["caranddriver.com"]
    start_urls = ["http://www.caranddriver.com/volkswagen/golf-r",]

    def parse(self, response):
        base_domain = "www.caranddriver.com"
        full_name_xpath = '//div[@id="overview--primary-submodel"]/h1/text()'
        full_name_response = Selector(response).xpath(full_name_xpath)

        photos_url_xpath = '//div[@id="overview--primary-submodel"]/div[2]/div[1]/a/@href'
        photos_url_response = Selector(response).xpath(photos_url_xpath)

        specs_url_xpath = '//div[@id="performance-data"]/div[2]/div[4]/a/@href'
        specs_url_response = Selector(response).xpath(specs_url_xpath)

        item = CarScrapyItem()
        item['name'] = full_name_response.extract()[0]
        item['img_url'] = photos_url_response.extract()[0]
        specs_url_extract = specs_url_response.extract()[0]
        specs_url_extract = base_domain + specs_url_extract

        #yield item, specs_url_extract
