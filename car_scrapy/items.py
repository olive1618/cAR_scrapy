"""Models"""
import scrapy


class CarScrapyItem(scrapy.Item):
    """Model for scraped data"""
    # identity stuff
    make = scrapy.Field()
    make_id = scrapy.Field()
    make_url_alias = scrapy.Field()
    model = scrapy.Field()
    model_id = scrapy.Field()
    model_url_alias = scrapy.Field()
    trim = scrapy.Field()
    trim_id = scrapy.Field()
    style = scrapy.Field()
    style_id = scrapy.Field()
    year = scrapy.Field()

    # URLs to store
    imgs_home_url = scrapy.Field()
    imgs_ng_callback = scrapy.Field()
    imgs_indv_url = scrapy.Field()

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

    #flag field to add imgs to first object. delete on yield.
    first = scrapy.Field()

    #flag field to use when processing lambda
    processed = scrapy.Field()


class TestItem(scrapy.Item):
    """Model for scraped data"""
    # identity stuff
    title = scrapy.Field()
    callstack = scrapy.Field()
    sedans = scrapy.Field()
    mazda = scrapy.Field()
    