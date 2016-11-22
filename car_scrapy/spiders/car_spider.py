"""
Instructions to spider for how to find exact data.

Scapy uses xpath selector patterns to find the desired elements to scrape.
"""

import re
from scrapy.selector import Selector
from scrapy import Spider
from scrapy.http import Request


class CarSpider(Spider):
    """Base class for spiders"""
    name = "car-spider"
    allowed_domains = ["caranddriver.com"]
    start_urls = ["http://www.caranddriver.com/volkswagen/golf-r",]

    def parse(self, response):
        base_domain = "www.caranddriver.com"
        sel = Selector(response)

        # Full name: make, model, & possiblly trim/package. Match to regex. Flag if error.
        full_name_xpath = '//div[@id="overview--primary-submodel"]/h1/text()'
        full_name_response = sel.xpath(full_name_xpath).extract()[0]
        full_name_error = False
        re_name = re.compile('([\\-\\S/]+)')
        if not re_name.match(full_name_response):
            full_name_error = True

        # Photos url to be used later to scrape images. Match to regex. Flag if error.
        photos_url_xpath = '//div[@id="overview--primary-submodel"]/div[2]/div[1]/a/@href'
        photos_url_response = sel.xpath(photos_url_xpath).extract()[0]
        photos_url_error = False
        re_photos_url = re.compile('http://www\\.caranddriver\\.com/photo-gallery/([\\-\\S/]+)')
        if not re_photos_url.match(photos_url_response):
            photos_url_error = True

        # Crawl chain from car's home page to its specs page using callback
        # Match url to regex.
        specs_url_xpath = '//div[@id="performance-data"]/div[2]/div[4]/a/@href'
        specs_url_response = sel.xpath(specs_url_xpath).extract()[0]
        specs_url_response = base_domain + specs_url_response
        re_specs_url = re.compile('http://www\\.caranddriver\\.com/([\\-\\S/]+)/specs')
        if re_specs_url.match(specs_url_response):
            yield Request(url=specs_url_response, callback=parse_specs)

        yield {
            'full_name': full_name_response,
            'full_name_flag': full_name_error,
            'photos_url': photos_url_response,
            'photos_url_flag': photos_url_error,
        }

    def parse_specs(self, response):
        pass
