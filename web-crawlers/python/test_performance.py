import subprocess
import os
from time import sleep
import tempfile
from pathlib import Path
from random import sample
import timeit

# from . import crawl

def generate_page(links: list[int]) -> str:
    return f"""
    <html><head></head><body><a href="/index.html">Index</a>{"".join([f'<a href="page_{link}.html">{link}</a>' for link in links])}</body></html>
    """


# def test_scrapes_large_site_many_times_and_measures_average_performance():
    
#     sleep(1)
#     try:
#         result = crawl("http://localhost:9876")
#         assert result == {'http://localhost:9876': ['http://localhost:9876/web-page.html'],
#                           'http://localhost:9876/web-page.html': []}
#     finally:
#         p.kill()

if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        # Generate page
        page_ids = list(range(0, 100))
        for page_number in page_ids:
            with open(temp_dir_path / f"page_{page_number}.html", "w") as f:
                f.write(generate_page(sample(page_ids, 10)))
        with open(temp_dir_path / "index.html", "w") as f:
            f.write(generate_page(sample(page_ids, 10)))
        # Start hosting

        p = subprocess.Popen(["python", "-m", "http.server", "9876"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=temp_dir)

        sleep(1)

        TRIES = 5
        try:
            # start timer
            result = timeit.timeit(f'crawl("http://localhost:9876")', setup='from crawler import crawl', number=TRIES)
            print(result / TRIES)
        finally:
            p.kill()