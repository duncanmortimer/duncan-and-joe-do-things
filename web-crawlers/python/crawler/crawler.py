from urllib.parse import urlparse
from typing import Callable, List, Generator

class Crawler:
    def __init__(self, get_links_for_url: Callable[[str], List[str]]) -> None:
        self.get_links_for_url = get_links_for_url

    @staticmethod
    def is_internal_url(url: str, starting_url: str):
        parsed_url = urlparse(url)
        parsed_starting_url = urlparse(starting_url)

        return parsed_url.hostname == parsed_starting_url.hostname
    
    def _crawl(self, starting_url: str) -> Generator[tuple[str, List[str]], None, None]:
        urls_to_crawl = [starting_url]
        while urls_to_crawl:
            url = urls_to_crawl.pop(0)
            links = self.get_links_for_url(url)
            internal_links = [link for link in links if self.is_internal_url(link, starting_url)]
            urls_to_crawl += internal_links
            yield (url, links)

    def crawl(self, starting_url: str) -> dict[str, List[str]]:
        return {url: links for url, links in self._crawl(starting_url)}