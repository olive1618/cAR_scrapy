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
            request = Request(specs_url_response, callback=self.parse_specs)
            request.meta['item'] = item
            yield request

    def parse_specs(self, response):
        """
        Parse the specs for the model.
        TODO Each style/trim combination has its own specs. Add code to handle.
        """
        item = response.meta['item']
        sel = Selector(response)

        style_options = sel.xpath('//select[@id="changeBodyStyle"]/option')
        item['style'] = style_options

        trim_options = sel.xpath('//select[@id="changeTrim"]/option[1]')
        item['trim'] = trim_options

        body_style_xpath = '//div[@id="content"]/div[5]/div[1]/table/tbody/tr[2]/td[2]/text()'
        body_style_response = sel.xpath(body_style_xpath).extract()[0]
        item['body_style'] = body_style_response

        num_passengers_xpath = '//div[@id="content"]/div[5]/div[1]/table/tbody/tr[16]/td[2]/text()'
        num_passengers_response = sel.xpath(num_passengers_xpath).extract()[0]
        item['num_passengers'] = num_passengers_response

        engine_type_xpath = '//div[@id="content"]/div[5]/div[1]/table/tbody/tr[31]/td[2]/text()'
        engine_type_response = sel.xpath(engine_type_xpath).extract()[0]
        item['engine_type'] = engine_type_response

        hp_at_rpm_xpath = '//div[@id="content"]/div[5]/div[1]/table/tbody/tr[34]/td[2]/text()'
        hp_at_rpm_response = sel.xpath(hp_at_rpm_xpath).extract()[0]
        item['hp_at_rpm'] = hp_at_rpm_response

        drivetrain_xpath = '//div[@id="content"]/div[5]/div[1]/table/tbody/tr[37]/td[2]/text()'
        drivetrain_response = sel.xpath(drivetrain_xpath).extract()[0]
        item['drivetrain'] = drivetrain_response

        transmission_xpath = '//div[@id="content"]/div[5]/div[1]/table/tbody/tr[39]/td[2]/text()'
        transmission_response = sel.xpath(transmission_xpath).extract()[0]
        item['transmission'] = transmission_response

        mpg_hwy_xpath = '//div[@id="content"]/div[5]/div[1]/table/tbody/tr[75]/td[2]/text()'
        mpg_hwy_response = sel.xpath(mpg_hwy_xpath).extract()[0]
        item['mpg_hwy'] = mpg_hwy_response

        mpg_city_xpath = '//div[@id="content"]/div[5]/div[1]/table/tbody/tr[77]/td[2]/text()'
        mpg_city_response = sel.xpath(mpg_city_xpath).extract()[0]
        item['mpg_city'] = mpg_city_response

        num_doors_xpath = '//div[@id="content"]/div[2]/p[2]/text()'
        num_doors_response = sel.xpath(num_doors_xpath).extract()[0]
        num_doors_list = num_doors_response.split(',')
        num_doors_matching = [s for s in num_doors_list if 'doors' in s][0]
        item['num_doors'] = num_doors_matching

        yield item
