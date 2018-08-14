from scrapy.spiders import CrawlSpider, Rule, Spider
from scrapy import http
from datetime import datetime
import json
import logging
import random
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

ua = UserAgent()
UA_HEADERS_LIST = [ua.chrome, ua.google, ua['google chrome'], ua.firefox, ua.ff]

logger = logging.getLogger(__name__)

try:
    from Appanie.Appanie.items import PublishedApp, VersionApp
except ImportError:
    from ..items import PublishedApp, VersionApp

try:
    from Appanie.Appanie.utils import load_json, generate_relative_path
except ImportError:
    from ..utils import load_json, generate_relative_path


class CompanyScraper(CrawlSpider):

    name = 'CompanyScraper'

    def __init__(self, company_id='gismart', start_date='2017-07-11', end_date='2018-07-11'):
        super(CompanyScraper, self).__init__()
        logger.info(company_id)
        self.company_id = company_id
        # transform dates string representations to datetime obj
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d')
        self.config = load_json(generate_relative_path(__file__, 'configs/company_crawler.json'))
        # login user and save user's session
        self.http_client = self._init_session()

    def _init_session(self):
        """
        Initializes user's session with appannie
        :return: http session
        """
        headers = {
            'Referer': self.config['page']['login'],
            'User-Agent': random.choice(UA_HEADERS_LIST)
        }
        client = requests.session()
        login = client.get(self.config['page']['login'], headers=headers)
        og_soup = BeautifulSoup(login.text, "html.parser")
        csrf_token = og_soup.find("input", value=True)["value"]
        payload = {
            'csrfmiddlewaretoken': csrf_token,
            'next': '/dashboard/home/',
            'username': self.config['user']['email'],
            'password': self.config['user']['password']
        }
        login_post = client.post(self.config['page']['login'], data=payload, headers=headers)
        return client

    def start_requests(self):
        url, h = self.gen_next_page(0)
        cookies = self.http_client.cookies.get_dict()
        yield http.Request(url, headers=h, cookies=cookies, meta={'dont_merge_cookies': True}, callback=self.parse_page)

    def parse_page(self, response):
        logger.info(response)
        cookies = self.http_client.cookies.get_dict()
        # parsing response body
        if response.body and response.body.__class__ == bytes:
            data = json.loads(response.body.decode('utf-8'))
            rows = data['data']['table']['rows']
            for row in rows:
                published_app = PublishedApp.from_row_data(row)
                for version in self.parse_app_versions(published_app):
                    yield version
                yield published_app
            if len(rows) == 0:
                yield None
            else:
                next_page_index = data['data']['table']['pagination']['current'] + 1
                url, h = self.gen_next_page(next_page_index)
                yield http.Request(url, headers=h, cookies=cookies, meta={'dont_merge_cookies': True},
                                   callback=self.parse_page)
        else:
            yield None

    def parse_app_versions(self, application):
        app_url = ''.join([self.config['page']['home'], application['url']])
        headers = self._get_authorized_headers()
        cookies = self.http_client.cookies.get_dict()
        headers["Cookie"] = "; ".join([str(x) + "=" + str(y) for x, y in cookies.items()])
        x = requests.get(app_url, headers=headers)
        soup = BeautifulSoup(x.text, "lxml")
        versions = soup.find_all('h5')
        for version in versions:
            yield VersionApp.from_soup(version, application)

    def gen_next_page(self, index, interval=50):
        company_id = self.company_id
        page_url = self.config['page']['company'].format(company_id, index, interval)
        headers = self._get_authorized_headers()
        return page_url, headers

    def _get_authorized_headers(self):
        return {
            'Referer': 'https://www.appannie.com/company/{}/'.format(self.company_id),
            'authority': 'www.appannie.com',
            'x-requested-with': 'XMLHttpRequest',
            'User-Agent': random.choice(UA_HEADERS_LIST)
        }