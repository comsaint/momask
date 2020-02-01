"""
scraper for https://www.ssm.gov.mo/apps1/apps/phquery/phqmaskstock.aspx
"""
from bs4 import BeautifulSoup
import requests
import time
from settings import CUR_TIMESTAMP, DATA_FOLDER


def make_request():
    """
    request the url to mask data.
    :return: requests.get() object to the url
    """
    base_url = 'https://www.ssm.gov.mo/apps1/apps/phquery/phqmaskstock.aspx'
    params = {'f': 'GetDataList',
              'time': int(time.time()*1000),  # timestamp in millisecond
              'dlimit': 0,
              'pg': 0,
              'ph': 'true',
              'issyncmask': 'false',
              'dorder': 'cast(code+as+integer)+asc',
              'sid': '',
              'apptype': ''
              }
    params_url = '&'.join('{}={}'.format(k,v) for k,v in params.items())  # too bad `requests` will urlencode the `dorder` param...
    return requests.get('?'.join([base_url, params_url]))


def write_scraped_file(r, path):
    soup = BeautifulSoup(r.content, 'lxml')  # parse content
    elem = soup.find_all('p')[0]  # get the JSON data
    with open(path, 'w', encoding='utf-8') as f:
        f.write(elem.text)
    return 0


def run_scraper():
    r = make_request()  # make request
    p = DATA_FOLDER / 'scraped_{}.txt'.format(CUR_TIMESTAMP)
    write_scraped_file(r, path=p)
    return p
