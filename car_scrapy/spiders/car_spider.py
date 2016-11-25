"""
Instructions to spider for how to find exact data.
Scapy uses xpath selector patterns to find the desired elements to scrape.
"""
import re
from scrapy.selector import Selector
from scrapy import Spider
from scrapy.http import Request
from car_scrapy.items import CarScrapyItem


class CarSpider(Spider):
    """Base class for spiders"""
    name = "car-spider"
    allowed_domains = ["http://www.caranddriver.com"]
    start_urls = ["http://www.caranddriver.com/volkswagen/golf-r",]

    def parse(self, response):
        """
        Parse the full name, photos url, and the specs url for a given make/model.
        Callback to parse specs from new request.
        """
        base_domain = "http://www.caranddriver.com"
        sel = Selector(response)
        item = CarScrapyItem()

        # Full name: make, model, & possiblly trim/package. Match to regex. Flag if error.
        full_name_xpath = '//div[@id="overview--primary-submodel"]/h1/text()'
        full_name_response = sel.xpath(full_name_xpath).extract()[0]
        full_name_error = False
        re_name = re.compile('([\\-\\S/]+)')
        if not re_name.match(full_name_response):
            full_name_error = True
        item['full_name_error'] = full_name_error
        item['full_name'] = full_name_response

        # Photos url to be used later to scrape images. Match to regex. Flag if error.
        photos_url_xpath = '//div[@id="overview--primary-submodel"]/div[2]/div[1]/a/@href'
        photos_url_response = sel.xpath(photos_url_xpath).extract()[0]
        photos_url_error = False
        re_photos_url = re.compile('http://www\\.caranddriver\\.com/photo-gallery/([\\-\\S/]+)')
        if not re_photos_url.match(photos_url_response):
            photos_url_error = True
        item['photos_url_error'] = photos_url_error
        item['photos_url'] = photos_url_response

        # Crawl chain from car's home page to its specs page using callback
        # Match url to regex.
        specs_url_xpath = '//div[@id="performance-data"]/div[2]/div[4]/a/@href'
        specs_url_response = sel.xpath(specs_url_xpath).extract()[0]
        specs_url_response = base_domain + specs_url_response
        re_specs_url = re.compile('http://www\\.caranddriver\\.com/([\\-\\S/]+)/specs')
        if re_specs_url.match(specs_url_response):
            item['specs_url'] = specs_url_response
            request = Request(url=specs_url_response, meta={'item':item}, callback=self.parse_specs)
        yield request
        print(request)

    def parse_specs(self, response):
        """
        Parse the specs for the model.
        TODO Each style/trim combination has its own specs. Add code to handle.
        """
        item = response.meta['item']
        sel = Selector(response)

        style_xpath = '//select[@id="changeBodyStyle"]/option[0]'
        item['style'] = sel.xpath(style_xpath).extract()[0]

        trim_xpath = '//select[@id="changeTrim"]/option[0]'
        item['trim'] = sel.xpath(trim_xpath).extract()[0]
        print('in specs\n', item)
        return item
