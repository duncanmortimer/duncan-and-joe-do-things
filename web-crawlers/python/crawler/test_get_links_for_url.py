from get_links_for_url import make_get_links_for_url


def test_should_return_empty_list_for_page_with_no_links():
    def mock_http_client(url: str) -> str:
        return "<html></html>"

    get_links_for_url = make_get_links_for_url(mock_http_client)

    assert get_links_for_url("http://www.example.com/") == []


def test_should_return_list_with_link_when_it_appears_in_html():
    def mock_http_client(url: str) -> str:
        return '<html><body><a href="http://www.example.com/hello">World</a></body></html>'

    get_links_for_url = make_get_links_for_url(mock_http_client)

    assert get_links_for_url("http://www.example.com/") == ["http://www.example.com/hello"]


def test_should_return_fully_resolved_urls():
    def mock_http_client(url: str) -> str:
        return '<html><body><a href="/hello">World</a></body></html>'

    get_links_for_url = make_get_links_for_url(mock_http_client)

    assert get_links_for_url("http://www.example.com/") == ["http://www.example.com/hello"]
