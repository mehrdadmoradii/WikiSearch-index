from unittest import TestCase
from WikiFetcher import WikiFetcher
import requests
from bs4 import BeautifulSoup


class TestWikiFetcher(TestCase):

    def setUp(self) -> None:
        self.wf = WikiFetcher()

    def test_fetch(self):
        urls = ['https://en.wikipedia.org/wiki/Computer_science', 'https://en.wikipedia.org/wiki/Computation', 'https://en.wikipedia.org/wiki/Arithmetic']

        for url in urls:
            output_paragraphs = self.wf.fetch(url)
            test_page = requests.get(url)
            test_page_beautiful = BeautifulSoup(test_page.content, 'html.parser')
            expected = test_page_beautiful.find(id='mw-content-text').findAll('p')
            self.assertEqual(output_paragraphs, expected)