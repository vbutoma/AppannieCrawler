# -*- coding: utf-8 -*-

from scrapy import Item, Field
from datetime import datetime, date

MIN_DATE = datetime.strptime('1900-01-01', '%Y-%m-%d')
MAX_DATE = datetime.strptime('2100-01-01', '%Y-%m-%d')


class PublishedApp(Item):
    name = Field()
    url = Field()
    release_date = Field()
    publisher = Field()

    def __init__(self,  name=None, url=None, release_date=None, publisher=None):
        super(PublishedApp, self).__init__()
        self['name'] = name
        self['url'] = url
        self['publisher'] = publisher
        self['release_date'] = release_date

    @classmethod
    def from_row_data(cls, row):
        name = row[0][0]
        url = row[0][2]
        publisher = row[1][0]
        release_date = datetime.strptime(row[3], '%b %d, %Y')
        return cls(
            name=name,
            url=url,
            release_date=release_date,
            publisher=publisher
        )

    def check_date(self, start_date=MIN_DATE, end_date=MAX_DATE):
        return start_date <= self['release_date'] <= end_date


class VersionApp(Item):
    version = Field()
    creation_date = Field()
    application = Field()

    def __init__(self, app=None, creation_date=None, version=None):
        super(VersionApp, self).__init__()
        self['application'] = app
        self['creation_date'] = datetime.strptime(creation_date, '%b %d, %Y')
        self['version'] = version

    @classmethod
    def from_soup(cls, soup, app):
        start_index = soup.contents[0].find('(')
        version = soup.contents[0][:start_index]
        creation_date = soup.contents[0][start_index + 1:-1]
        return cls(
            app=app['name'],
            creation_date=creation_date,
            version=version
        )

    def check_date(self, start_date=MIN_DATE, end_date=MAX_DATE):
        return start_date <= self['creation_date'] <= end_date
