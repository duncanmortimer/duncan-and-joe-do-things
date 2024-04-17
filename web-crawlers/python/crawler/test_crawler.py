import pytest
from crawler import Crawler
from typing import List


def test_scrapes_page_with_no_internal_links():
    starting_url = 'http://example.com'
    expected_urls = ['http://another-example.com/example']
    def mock_link_getter(url: str) -> List[str]:
        match url:
            case 'http://example.com':
                return expected_urls
            case _:
                pytest.fail('Should not fetch external URLs')

    crawler = Crawler(mock_link_getter)

    result = crawler.crawl(starting_url)

    assert starting_url in result
    assert result.get(starting_url) == expected_urls


def test_scrapes_page_and_follows_internal_link():
    starting_url = 'http://example.com'

    def mock_link_getter(url: str) -> List[str]:
        match url:
            case 'http://example.com':
                return ['http://example.com/another_page']
            case 'http://example.com/another_page':
                return []
            case _: return []

    crawler = Crawler(mock_link_getter)

    result = crawler.crawl(starting_url)

    assert result.get(starting_url) == ['http://example.com/another_page']
    assert result.get('http://example.com/another_page') == []


def test_scrapes_page_and_follows_internal_secure_link():
    starting_url = 'http://example.com'

    def mock_link_getter(url: str) -> List[str]:
        match url:
            case 'http://example.com':
                return ['https://example.com/another_page']
            case 'https://example.com/another_page':
                return []
            case _: return []

    crawler = Crawler(mock_link_getter)

    result = crawler.crawl(starting_url)

    assert result.get(starting_url) == ['https://example.com/another_page']
    assert result.get('https://example.com/another_page') == []
