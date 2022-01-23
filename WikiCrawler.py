from CicularQueue import CircularQueue as QueueFrontier
from WikiFetcher import WikiFetcher
from TermCounter import TermCounter
from Index import Index
from RedisMaker import make
from bs4 import BeautifulSoup


class WikiCrawler:
    """Provide methods to perform breadth-first traversal of the given Wikipedia URL and index the page"""

    __slots__ = ('_frontier', '_start', '_number_of_iteration',
                 '_wiki_fetcher', '_index', '_visited_pages', '_redis_connection')

    def __init__(self, start, number_of_iteration):
        self._start = start
        self._number_of_iteration = number_of_iteration
        self._frontier = QueueFrontier()
        self._frontier.enqueue(self._start)
        self._wiki_fetcher = WikiFetcher()
        self._redis_connection = make()
        self._index = Index(self._redis_connection)
        self._visited_pages = self.cache_visited_pages()  # caching the indexed pages from database

    def cache_visited_pages(self):
        return ({link.decode('utf-8') for link in
                self._redis_connection.keys('TermCounter:*')})  # using set to achieve O(1) lookup

    def redis_term_counter_key(self, term):
        return 'TermCounter:' + term

    def is_visited(self, url):
        term_counter_key = self.redis_term_counter_key(url)
        return term_counter_key in self._visited_pages

    def add_to_visited(self, url):
        term_counter_key = self.redis_term_counter_key(url)
        self._visited_pages.add(term_counter_key)

    def make_local_link_global(self, link):
        return 'https://en.wikipedia.org' + link

    def crawl(self):
        current_url = self._frontier.dequeue()

        while self._number_of_iteration > 0:
            print(f'Crawling... {current_url}')
            try:
                paragraphs = self._wiki_fetcher.fetch(current_url)
                self._parse_paragraphs(paragraphs)   # expanding the frontier
                if not self.is_visited(current_url):
                        term_counter = TermCounter(current_url)
                        term_counter.process_paragraphs(paragraphs)
                        self._index.process_term_counter(term_counter)
                        self._number_of_iteration -= 1
                        self.add_to_visited(current_url)
                        print(f'Indexing {current_url} done!')
                else:
                    print(f'{current_url} is already indexed!')
            except Exception:
                print(f'An error occurred while indexing {current_url}')
            if not self._frontier.is_empty():
                current_url = self._frontier.dequeue()

    def _parse_paragraphs(self, paragraphs):
        for p in paragraphs:
            self._expand_links(p)

    def _expand_links(self, paragraph: BeautifulSoup):
        for p in paragraph.findAll('a'):
            if not (p['href'].startswith('/wiki/')):
                continue
            global_url = self.make_local_link_global(p['href'])
            if self.is_visited(global_url):
                continue
            if '#' in global_url:
                global_url = (global_url.split('#')[0])
            self._frontier.enqueue(global_url)


def main():
    start = 'https://en.wikipedia.org/wiki/Python_(programming_language)'
    number_of_iteration = 300
    crawler = WikiCrawler(start, number_of_iteration)
    crawler.crawl()


if __name__ == '__main__':
    main()
