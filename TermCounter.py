import string

from bs4 import BeautifulSoup
from WikiNodeIterable import WikiNodeIterable
import bs4.element
from nltk.corpus import stopwords


class TermCounter:
    """Provides method to parse `BeautifulSoup` paragraph and count it terms"""

    __slots__ = '_map', '_name', '_stop_words'

    def __init__(self, page_name: str):
        self._name = page_name
        self._map: dict[str, int] = dict()
        self._stop_words = set(stopwords.words('english'))

    def get_name(self) -> str:
        """Returns the name of the webpage associated with this class"""
        return self._name

    def get_count(self, term: str) -> int:
        """Returns the number of times the given term appeared in the counter"""
        if not (term in self._map):
            return 0
        return self._map[term]

    def get_terms(self) -> list[str]:
        """Returns the list of terms that exist in the counter"""
        keys = self._map.keys()
        return list(keys)

    def has_term(self, term: str):
        """Returns true if the given term appeared in the counter"""
        return term in self._map

    def process_paragraphs(self, paragraphs: [BeautifulSoup]):
        for paragraph in paragraphs:
            self._process_paragraph(paragraph)

    def _process_paragraph(self, paragraph: BeautifulSoup):
        wiki_node_iterable = WikiNodeIterable(paragraph)
        for node in wiki_node_iterable:
            if type(node) == bs4.element.NavigableString:
                self._process_sentence(node)

    def _process_sentence(self, sentence):
        text_array = sentence.split(" ")
        for text in text_array:
            clean_text = self.remove_punctuation_and_text_from_text(text)
            if len(clean_text) == 0:
                continue
            if clean_text in self._stop_words:
                continue
            self._increment_count(clean_text)    # incrementing term count

    def _increment_count(self, term: str):
        if term in self._map:
            count = self._map[term]
            self._map[term] = count+1
        else:
            self._map[term] = 1

    def remove_punctuation_and_text_from_text(self, text: str) -> str:
        clean_text = ''
        for ch in text:
            ascii_value = ord(ch)
            if (65 <= ascii_value <= 90) or (97 <= ascii_value <= 122) or ascii_value == 39:
                clean_text += ch
        return clean_text.lower()


from WikiFetcher import WikiFetcher
if __name__ == '__main__':
    url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'
    paragraphs = WikiFetcher().fetch(url)
    tc = TermCounter('Python_(programming_language)')
    tc.process_paragraphs(paragraphs)
    # print(tc.has_term('c++'))
    for key in tc.get_terms():
        print(key)
