class Crawler:
    def __init__(self, get_links_for_url) -> None:
        self.get_links_for_url = get_links_for_url
    
    def crawl(self, starting_url):
        urls_to_crawl = [starting_url]
        result = {}
        while urls_to_crawl:
            url = urls_to_crawl.pop(0)
            links = self.get_links_for_url(url)
            internal_links = [link for link in links if starting_url in link]
            urls_to_crawl += internal_links
            result[url] = links
        return result