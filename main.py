import random
import requests

from fake_useragent import UserAgent
from bs4 import BeautifulSoup

import sys

ua = UserAgent()
UA_HEADERS_LIST = [ua.chrome, ua.google, ua['google chrome'], ua.firefox, ua.ff]

if __name__ == "__main__":
    headers = {
        'Referer': 'https://www.appannie.com/account/login/',
        'User-Agent': UA_HEADERS_LIST[0]
    }
    print(headers)

    client = requests.session()
    login_url = 'https://www.appannie.com/account/login/'
    login = client.get(login_url, headers=headers)
    print('################################')
    print(client.cookies)
    print('################################')
    og_soup = BeautifulSoup(login.text, "html.parser")

    csrf_token = og_soup.find("input", value=True)["value"]
    print(csrf_token)

    with open('creds.txt') as f:
        credentials = [x.strip('\n') for x in f.readlines()]
    username = credentials[0]
    password = credentials[1]
    payload = {
        'csrfmiddlewaretoken': csrf_token,
        'next': '/dashboard/home/',
        'username': username,
        'password': password
    }

    login_post = client.post(login_url, data=payload, headers=headers)
    print('################################')
    print(client.cookies.get_dict())
    print('################################')
    print("Login response is: " + str(login_post.status_code))

    # fb = 1000200000000034
    headers['Referer'] = 'https://www.appannie.com/company/1000200000000034/'
    headers['authority'] = 'www.appannie.com'
    headers['x-requested-with'] = 'XMLHttpRequest'
    # headers['accept'] = 'application/json, text/javascript, */*; q=0.01'
    # headers['accept-encoding'] = 'gzip, deflate, br'
    # headers['x-newrelic-id'] = 'VwcPUFJXGwEBUlJSDgc='
    # headers['accept-language'] = 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
    comp = 'https://www.appannie.com/ajax/company/1000200000000034/apps/table_data/?page=0&page_interval=10&orderby=app_with_links&desc=f'
    comp = 'https://www.appannie.com/apps/ios/app/ar-studio-player/details/'
    # x = client.get(comp, headers=headers)
    cookies = client.cookies.get_dict()
    headers["Cookie"] = cookie_string = "; ".join([str(x) + "=" + str(y) for x, y in cookies.items()])
    x = requests.get(comp, headers=headers)
    print('################################')
    print(client.cookies)
    print('################################')
    print(x.status_code)
    with open('page_details.html', 'w') as page:
        page.write(x.text)
    print(x.text)

    a = 1

