# -*- coding: utf-8 -*-
import json
import logging
import pandas as pd
import scrapy
from .items import PublishedApp, VersionApp

logger = logging.getLogger(__name__)


def dict_class_fields(cls):
    return dict([(k, []) for k in cls.fields.keys()])


class CsvPipeline(object):

    def __init__(self):
        self.count = 0
        # this list should contain scrapy.Item subclasses
        self.classes = [PublishedApp, VersionApp]
        self.files = {(cls.__name__, None) for cls in self.classes}
        self.data_frames = dict([(cls.__name__, dict_class_fields(cls)) for cls in self.classes])

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        for cls in self.classes:
            class_name = cls.__name__
            df = pd.DataFrame(data=self.data_frames[class_name])
            df.to_csv('{}.csv'.format(class_name), sep='|', index=False)
            message = 'Different {} count: {} for period {} ... {}'.format(
                class_name, len(df), spider.start_date, spider.end_date)
            logger.info(message)

    def process_item(self, item, spider):
        try:
            class_name = type(item).__name__
            if item.check_date(spider.start_date, spider.end_date):
                for k in self.data_frames[class_name].keys():
                    self.data_frames[class_name][k].append(item[k])
            self.pipe_item(item)
        except KeyError:
            logger.error('No handler for item class {}'.format(type(item).__name__))

    def pipe_item(self, item):
        self.count += 1
        if self.count % 10 == 0:
            logger.info('{} processed items !'.format(self.count))