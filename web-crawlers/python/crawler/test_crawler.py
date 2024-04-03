from crawler import Crawler

def test_scrapes_page_with_no_internal_links():
    starting_url = 'http://example.com'
    expected_urls = ['http://another-example.com/example']
    mock_http_client = lambda _: expected_urls

    crawler = Crawler(mock_http_client)

    result = crawler.crawl(starting_url)  # Dict[Url, List[Url]]

    assert starting_url in result
    assert result.get(starting_url) == expected_urls