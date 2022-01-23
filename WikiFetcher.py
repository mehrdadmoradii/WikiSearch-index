import requests
from bs4 import BeautifulSoup
import time


class WikiFetcher:
    """Provide methods to grab main paragraphs of a given Wikipedia page"""

    __slots__ = 'last_fetch_time'

    def __init__(self):
        self.last_fetch_time = -1

    def sleep(self):
        """Makes sure there's always 1 second gap between eeach fetch"""
        current_time = time.time_ns() / 1000000  # current time in millisecond
        if self.last_fetch_time != -1:
            remaining_time = current_time - self.last_fetch_time
            if remaining_time < 1000:
                time.sleep(remaining_time / 1000)
        self.last_fetch_time = current_time

    def fetch(self, url: str) -> BeautifulSoup:
        """Fetches the main paragraphs of a given Wikipedia page URL"""
        self.sleep()
        page = requests.get(url)
        beautiful_page = BeautifulSoup(page.content, 'html.parser')
        main_content = beautiful_page.find(id='mw-content-text')
        paragraphs = main_content.findAll('p')
        return paragraphs


if __name__ == '__main__':
    wf = WikiFetcher()
    print('\n fetching page 1...\n')
    abc = wf.fetch("https://en.wikipedia.org/wiki/Python_(programming_language)")
    print(abc)


    print('\n fetching page 2...\n')
    defg = wf.fetch('https://en.wikipedia.org/wiki/Interpreter_(computing)')
    print(defg)

    print('\n fetching page 3...\n')
    hij = wf.fetch('https://en.wikipedia.org/wiki/Computer_science')
    print(hij)
