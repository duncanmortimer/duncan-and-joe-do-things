from bs4 import BeautifulSoup
from typing import List, Callable
from urllib.parse import urljoin

def make_get_links_for_url(http_client: Callable[[str], str]):
    def get_links_for_url(url: str) -> List[str]:
        page_text = http_client(url)
        soup = BeautifulSoup(page_text, "html.parser")
        anchors = soup.find_all("a")
        return [urljoin(url, anchor.get('href')) for anchor in anchors]

    return get_links_for_url