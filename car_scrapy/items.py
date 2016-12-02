"""Models"""
import scrapy


class CarScrapyItem(scrapy.Item):
    """Model for scraped data"""
    # identity stuff
    make = scrapy.Field()
    make_id = scrapy.Field()
    model = scrapy.Field()
    model_id = scrapy.Field()
    trim = scrapy.Field()
    trim_id = scrapy.Field()
    style = scrapy.Field()
    style_id = scrapy.Field()
    year = scrapy.Field()
    style_trim = scrapy.Field()

    # URLs to store
    photos_url = scrapy.Field()

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
