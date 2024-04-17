import subprocess
import os
from time import sleep

from . import crawl


def test_scrapes_page_from_simple_site():
    dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures/simple_site/')
    p = subprocess.Popen(["python", "-m", "http.server", "9876"], cwd=dir_path)
    sleep(1)
    try:
        result = crawl("http://localhost:9876")
        assert result == {'http://localhost:9876': ['http://localhost:9876/web-page.html'],
                          'http://localhost:9876/web-page.html': []}
    finally:
        p.kill()
