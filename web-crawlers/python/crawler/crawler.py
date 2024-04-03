class Crawler:
    def __init__(self, get_links_for_url) -> None:
        self.get_links_for_url = get_links_for_url
    
    def crawl(self, starting_url):
        urls_to_crawl = [starting_url]
        result = {}
        while urls_to_crawl:
            url = urls_to_crawl.pop(0)
            links = self.get_links_for_url(url)
            urls_to_crawl += links
            result[url] = links
        return result