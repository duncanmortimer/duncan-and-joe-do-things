import requests

from .crawler import Crawler
from .get_links_for_url import make_get_links_for_url

def http_client(url: str) -> str:
    result = requests.get(url)

    return result.text

def crawl(url: str):
    crawler = Crawler(make_get_links_for_url(http_client))

    return crawler.crawl(url)