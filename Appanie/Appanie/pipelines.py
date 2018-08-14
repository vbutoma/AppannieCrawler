# -*- coding: utf-8 -*-
import json
import logging
import pandas as pd

from .items import PublishedApp, VersionApp

logger = logging.getLogger(__name__)


class CsvPipeline(object):

    def __init__(self):
        self.count = 0
        self.classes = [PublishedApp, VersionApp]
        # todo: init from class list
        self.files = {
            PublishedApp.__name__: None,
            VersionApp.__name__: None
        }

        self.data_frames = {
            PublishedApp.__name__: dict([(k, []) for k in PublishedApp.fields.keys()]),
            VersionApp.__name__: dict([(k, []) for k in VersionApp.fields.keys()])
        }

    def open_spider(self, spider):
        # for key in self.files.keys():
        #     self.files[key] = open('{}.csv'.format(key), 'w')
        pass

    def close_spider(self, spider):
        for cls in self.classes:
            class_name = cls.__name__
            df = pd.DataFrame(data=self.data_frames[class_name])
            df.to_csv('{}.csv'.format(class_name), sep='|', index=False)
            # self.files[class_name].close()

    def process_item(self, item, spider):
        try:
            class_name = type(item).__name__
            for k in self.data_frames[class_name].keys():
                self.data_frames[class_name][k].append(item[k])
            # file_desc = self.files[type(item).__name__]
            self.pipe_item(item)
            line = str(item) + '\n'
            # file_desc.write(line)
        except KeyError:
            logger.error('No handler for item class {}'.format(type(item).__name__))

    def pipe_item(self, item):
        self.count += 1
        if self.count % 10 == 0:
            logger.info(self.count)