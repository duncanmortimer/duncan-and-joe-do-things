class Crawler:
    def __init__(self, get_links_for_url) -> None:
        self.get_links_for_url = get_links_for_url
    
    def crawl(self, starting_url):
        return {starting_url: self.get_links_for_url(starting_url)}