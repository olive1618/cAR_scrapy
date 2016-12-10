"""Pipeline to process data to MongoDB collection"""
import logging
import pymongo
from scrapy.conf import settings
from scrapy.utils.log import configure_logging


class MongoPipeline(object):
    """MongoDB pipeline.  Currently using MongoDB hosted on home network"""
    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_HOST'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DATABASE']]
        self.collection = db[settings['MONGODB_COLLECTION']]
        configure_logging(install_root_handler=False)
        logging.basicConfig(filename=settings['LOG_FILE'], format='%(levelname)s: %(message)s',
                            level=settings['LOG_LEVEL'])

    def process_item(self, item, spider):
        """Insert item and write to log"""
        self.collection.insert(dict(item))
        return item
