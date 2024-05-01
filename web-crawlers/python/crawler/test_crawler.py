import pytest
from .crawler import Crawler
from typing import List, Callable


def test_should_not_follow_external_links():
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


def test_should_follow_internal_links():
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


def test_should_follow_internal_secure_link():
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


def test_should_not_revisit_pages():
    starting_url = 'http://example.com'

    def build_link_getter(results_map: dict[tuple[str, int], List[str] | Callable[[], None]]):
        visit_counter: dict[str, int] = {}
        def link_getter(url: str) -> List[str]:
            visits = visit_counter.get(url, 0)
            result = results_map.get((url, visits))
            visit_counter[url] = visits + 1
            if callable(result):
                result()
                return []
            elif result is None:
                pytest.fail("url not found in results map")
            else:
                return result
        return link_getter

    mock_link_getter = build_link_getter({
        (starting_url, 0): ['http://example.com/another_page'],
        (starting_url, 1): lambda: pytest.fail("Should not revisit page"),
        ('http://example.com/another_page', 0): ["http://example.com"]
    })

    crawler = Crawler(mock_link_getter)

    result = crawler.crawl(starting_url)

    assert result.get(starting_url) == ['http://example.com/another_page']
    assert result.get('http://example.com/another_page') == [starting_url]