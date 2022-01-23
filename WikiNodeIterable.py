from collections import deque
import bs4.element
from bs4 import BeautifulSoup
import requests


class WikiNodeIterable:
    """Implements a depth-first traversal of a given BeautifulSoup node"""

    __slots__ = '_stack'

    def __init__(self, root: BeautifulSoup):
        self._stack = deque()
        self._stack.append(root)

    def __iter__(self):
        return self

    def __next__(self):
        if len(self._stack) == 0:
            raise StopIteration
        newest = self._stack.pop()
        if type(newest) != bs4.element.NavigableString:
            if hasattr(newest, 'content'):
                child_nodes = newest.contents
                child_nodes.reverse()
                for child in child_nodes:
                    self._stack.append(child)
        return newest


if __name__ == '__main__':
    page = requests.get('https://en.wikipedia.org/wiki/Python_(programming_language)')
    main_page = BeautifulSoup(page.content, 'html.parser')
    paragraphs = main_page.find(id='mw-content-text').find_all('p')
    for node in WikiNodeIterable(paragraphs[1]):
        if type(node) == bs4.element.NavigableString:
            print(node)