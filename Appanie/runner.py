from scrapy import cmdline
import pandas as pd
import argparse
import sys

PUBLISHED_APPS_DATA = 'PublishedApp.csv'
APPS_VERSIONS_DATA = 'VersionApp.csv'


def scrape(company_id=1000200000020105, start_date='2017-08-01', end_date='2018-08-01'):
    command = 'scrapy crawl CompanyScraper -a company_id={} -a start_date={} -a end_date={}'\
        .format(company_id, start_date, end_date)
    cmdline.execute(command.split())


def calculate():
    pass


if __name__ == "__main__":
    scrape()

