"""
scraper for https://www.ssm.gov.mo/apps1/apps/phquery/phqmaskstock.aspx (pharmacy)
and https://www.ssm.gov.mo/apps1/apps/phquery/maskstock/hcmaskstock.aspx (hygiene centre)
"""
from bs4 import BeautifulSoup
import requests
import time
from settings import CUR_TIMESTAMP, DATA_FOLDER


def make_request_for_pharmacy():
    """
    request the url to mask data of pharmacy.
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


def make_request_for_health_centre():
    """
    request the url to mask data of health centre.
    :return: requests.get() object to the url
    """
    base_url = 'https://www.ssm.gov.mo/apps1/apps/phquery/maskstock/hcmaskstock.aspx'
    params = {'f': 'GetPHCMaskStock',
              'time': int(time.time() * 1000),  # timestamp in millisecond
              'dlimit': 0,
              'pg': 0,
              'dorder': 'cast(code as integer) asc',
              'sid': '',
              'apptype': ''
              }
    params_url = '&'.join(
        '{}={}'.format(k, v) for k, v in params.items())  # too bad `requests` will urlencode the `dorder` param...
    return requests.get('?'.join([base_url, params_url]))


def write_scraped_file(r, path):
    soup = BeautifulSoup(r.content, 'lxml')  # parse content
    elem = soup.find_all('p')[0]  # get the JSON data
    with open(path, 'w', encoding='utf-8') as f:
        f.write(elem.text)
    return 0


def run_scraper():
    r1 = make_request_for_pharmacy()  # make request for pharmacy
    p1 = DATA_FOLDER / 'scraped_phq_{}.txt'.format(CUR_TIMESTAMP)
    write_scraped_file(r1, path=p1)
    r2 = make_request_for_health_centre()
    p2 = DATA_FOLDER / 'scraped_hc_{}.txt'.format(CUR_TIMESTAMP)
    write_scraped_file(r2, p2)
    return p1, p2


run_scraper()
