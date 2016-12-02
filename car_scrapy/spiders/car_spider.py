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
        if re_photos_url.match(photos_url_response):
            item['photos_url'] = photos_url_response

        # Use xpath to get model ID and make.  Match with regex.
        make_model_xpath = '//div[@id="content"]/script/text()'
        make_model_response = sel.xpath(make_model_xpath).extract()[0]
        make = re.findall(r'\"(.+?)\"', make_model_response)[1]
        item['make'] = make
        model_id = re.findall(r'\"(.+?)\"', make_model_response)[0]
        item['model_id'] = model_id
        item['style_trim'] = {}

        # Pass pre-fab url with model ID embedded to callback to parse style info
        model_url = "http://www.caranddriver.com/api/vehicles/styles-by-model/{}/json?ddIgnore=1"
        model_url = model_url.format(model_id)
        request = Request(model_url, callback=self.parse_style, meta={'item':item})
        yield request

    def parse_style(self, response):
        """Object's keys are tuples of each style's ID, name, and year"""
        item = response.meta['item']
        json_response = json.loads(response.body_as_unicode())
        item['model'] = json_response['vehicles']['styles']['model_url_alias']
        # 'Groups' contains an array of dicts where each dict is a style
        num_styles = len(json_response['vehicles']['styles']['groups'])

        for i in range(num_styles):
            # Create shorthand for this style since lines are otherwise long
            this_style = json_response['vehicles']['styles']['groups'][i]
            # Will use style ID in JSON URL
            style_id = this_style["submodel_group_id"]
            # Style name is unique key for style
            style_name = this_style["groupname"]
            item['style_trim'][style_name] = {}
            # Pass item to callback to add this style's trim information
            trim_url = 'http://www.caranddriver.com/api/payments/trims-by-submodel-group'
            trim_url += '/{}/{}/json?ddIgnore=1'
            trim_url = trim_url.format(item['model_id'], style_id)
            request = Request(trim_url, callback=self.parse_trim, meta={'item':item})
            yield request

    def parse_trim(self, response):
        """Add trim sub-object to each style object"""
        item = response.meta['item']
        json_response = json.loads(response.body_as_unicode())

        # Use style name to pull particular dictionary
        style_name = json_response["alltrims"][0]["submodel_group_name"]
        this_style = item['style_trim'][style_name]  # this is a {}

        # Add style level ID and year
        style_id = json_response["alltrims"][0]["submodel_group_id"]
        this_style['style_id'] = style_id
        style_year = json_response["alltrims"][0]["year"]
        this_style['year'] = style_year

        num_trims = len(json_response["alltrims"])
        for i in range(num_trims):
            # Use trim name as unique key for this trim's info'
            trim_name = json_response["alltrims"][i]["friendly_name"]
            this_style[trim_name] = {}
            this_style[trim_name]['trim_id'] = json_response["alltrims"][i]["id"]
            this_style[trim_name]['msrp'] = json_response["alltrims"][i]["base_msrp"]
            this_trim = json_response['alltrims'][i]['chrome_data']
            this_style[trim_name]['num_passengers'] = this_trim['Passenger Capacity']['value']
            this_style[trim_name]['body_style'] = this_trim['EPA Classification']['value']
            this_style[trim_name]['mpg_hwy'] = this_trim['EPA Fuel Economy Est - Hwy']['value']
            this_style[trim_name]['mpg_city'] = this_trim['EPA Fuel Economy Est - City']['value']
            this_style[trim_name]['drivetrain'] = this_trim['Drivetrain']['value']
            this_style[trim_name]['engine_type'] = this_trim['Engine Type']['value']
            this_style[trim_name]['hp_at_rpm'] = this_trim['SAE Net Horsepower @ RPM']['value']
            this_style[trim_name]['transmission'] = this_trim['Trans Type']['value']

        yield item
