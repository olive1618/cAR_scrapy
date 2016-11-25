"""coding: utf-8"""

from scrapy import Item, Field


class CarScrapyItem(Item):
    """Model for scraped data"""
    # identity stuff
    full_name = Field()
    full_name_error = Field()
    trim = Field()
    year = Field()
    specs_url = Field()

    # images
    photos_url = Field()
    photos_url_error = Field()

    # basic car descriptors
    body_style = Field()
    num_passengers = Field()
    num_doors = Field()
    msrp = Field()

    # specs
    engine_type = Field()
    hp_at_rpm = Field()
    drivetrain = Field()
    transmission_type = Field()
    mpg_city = Field()
    mpg_hwy = Field()
