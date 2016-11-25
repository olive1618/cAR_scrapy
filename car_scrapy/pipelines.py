"""
 -*- coding: utf-8 -*-
"""

import json


class JsonWriterPipeline(object):
    """Pipeline to process scraped items and write to JSON file"""

    def open_spider(self, spider):
        self.file = open('items.jl', 'wb')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item


# class CarScrapyPipeline(object):
#     def process_item(self, item, spider):
#         return item
