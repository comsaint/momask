"""
scraper for https://www.ssm.gov.mo/apps1/apps/phquery/phqmaskstock.aspx
"""
from bs4 import BeautifulSoup
import requests
import time
import json


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


r = make_request()  # make request
soup = BeautifulSoup(r.content, 'lxml')  # parse content
elem = soup.find_all('p')[0]  # get the JSON data
with open('elem.txt', 'w', encoding='utf-8') as f:
    f.write(elem.text)

"""
# need a series parser...
parsed_json = parse_data(elem.text)
print(parsed_json)
"""

