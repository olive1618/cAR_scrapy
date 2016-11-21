"""coding: utf-8"""

import scrapy


class CarScrapyItem(scrapy.Item):
    """Model for scraped data"""
    file_urls = scrapy.Field()
    files = scrapy.Field()

    # identity stuff
    name = scrapy.Field()
    trim = scrapy.Field()
    year = scrapy.Field()

    # images
    img_url = scrapy.Field()

    # basic car descriptors
    body_style = scrapy.Field()
    num_passengers = scrapy.Field()
    num_doors = scrapy.Field()
    msrp = scrapy.Field()

    # specs
    engine_type = scrapy.Field()
    hp_at_rpm = scrapy.Field()
    drivetrain = scrapy.Field()
    transmission_type = scrapy.Field()
    mpg_city = scrapy.Field()
    mpg_hwy = scrapy.Field()
