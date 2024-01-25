# parse_wanfei.py

import json
import re
import sys
import urllib.parse
from pathlib import Path
from pprint import pprint

import requests
from bs4 import BeautifulSoup


# html_URL=r"https://www.wangfei.in/vodplay/106593-10-12.html"
U = 'https://www.wangfei.in/vodplay/106593-8-20.html'


def parse_wangfei(url):
    def _get_m3u8_url(json, key):
        m3u8_1_url = urllib.parse.unquote(json.get(key)).replace('https', 'http')  # e.g. 'https://vip.ffzy-online3.com/20230224/16767_d5f2a1de/index.m3u8'
        redirected = requests.get(m3u8_1_url).text.rsplit('\n', maxsplit=1)[-1]  # e.g. '2000k/hls/mixed.m3u8'

        _components = urllib.parse.urlparse(m3u8_1_url)
        new_url = urllib.parse.urlunparse(
            _components._replace(path=(Path(_components.path).parent / redirected).as_posix())  #
        )

        return new_url

    j = json.loads(
        BeautifulSoup(requests.get(url).text, 'html.parser')  #
        .find('script', string=re.compile('player_aaa'))
        .string.split('=', maxsplit=1)[-1]
    )

    this = _get_m3u8_url(j, 'url')
    next = _get_m3u8_url(j, 'url_next')

    return this, next


if __name__ == '__main__':
    url = sys.argv[1] if len(sys.argv) > 1 else U

    m3u8, next = parse_wangfei(url)

    pprint([m3u8, next])
