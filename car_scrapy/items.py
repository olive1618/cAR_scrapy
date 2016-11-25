"""Models"""
import scrapy


class CarScrapyItem(scrapy.Item):
    """Model for scraped data"""
    # identity stuff
    full_name = scrapy.Field()
    full_name_error = scrapy.Field()
    trim = scrapy.Field()
    style = scrapy.Field()
    year = scrapy.Field()
    specs_url = scrapy.Field()

    # images
    photos_url = scrapy.Field()
    photos_url_error = scrapy.Field()

    # basic car descriptors
    body_style = scrapy.Field()
    num_passengers = scrapy.Field()
    num_doors = scrapy.Field()
    msrp = scrapy.Field()

    # specs
    engine_type = scrapy.Field()
    hp_at_rpm = scrapy.Field()
    drivetrain = scrapy.Field()
    transmission = scrapy.Field()
    mpg_city = scrapy.Field()
    mpg_hwy = scrapy.Field()
