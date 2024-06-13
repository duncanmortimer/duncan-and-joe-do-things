from urllib.parse import urlparse
from asyncio import gather, run
from typing import Callable, List, Generator

import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin

MAX_TRIES = 0

async def get_links_async(url: str, session: aiohttp.ClientSession, tries: int = 0) -> List[str]:
    if tries > MAX_TRIES:
        raise Exception(f"Max tries exceeded for {url}")
    try:
        async with session.get(url) as response:
            print(f"Getting {url} ...")
            page_text = await response.text()
            soup = BeautifulSoup(page_text, "html.parser")
            anchors = soup.find_all("a")
            return [urljoin(url, anchor.get('href')) for anchor in anchors]
    except Exception as e:
        print('Error: ', e)
        return await get_links_async(url, session, tries + 1)

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
        crawled_urls: set[str] = set()
        while urls_to_crawl:
            urls = urls_to_crawl[:10]
            urls_to_crawl = urls_to_crawl[10:]
            
            async def get_urls():
                async with aiohttp.ClientSession() as session:
                    results = await gather(*[get_links_async(url, session) for url in urls])
                    return {url: links for url, links in zip(urls, results)}
            url_to_links_map = run(get_urls())
            crawled_urls = crawled_urls.union(urls)
            
            unique_links = set(link for links in url_to_links_map.values() for link in links)
            urls_to_crawl += [link for link in unique_links if link not in crawled_urls and self.is_internal_url(link, starting_url)]

            for url, links in url_to_links_map.items():
                yield (url, links)

    def crawl(self, starting_url: str) -> dict[str, List[str]]:
        return {url: links for url, links in self._crawl(starting_url)}
    


