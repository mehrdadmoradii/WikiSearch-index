from RedisMaker import make
from TermCounter import TermCounter
from WikiFetcher import WikiFetcher
import redis


class Index:
    """Provide methods for index"""

    __slots__ = '_redis'

    def __init__(self, redis_connection: redis.Redis):
        self._redis = redis_connection

    def _redis_url_set_key(self, url):
        return 'URLSet:' + url

    def _redis_term_counter_key(self, term):
        return 'TermCounter:' + term

    def is_indexed(self, term):
        term = self._redis_term_counter_key(term)
        return term in self._redis.keys('TermCounter:*')

    def process_term_counter(self, term_counter: TermCounter):
        term_counter_name = term_counter.get_name()
        redis_hash_key = self._redis_term_counter_key(term_counter_name)

        self._redis.delete(redis_hash_key)
        redis_pipeline = self._redis.pipeline()

        for key in term_counter.get_terms():
            redis_key = self._redis_url_set_key(key)
            redis_pipeline.sadd(redis_key, term_counter_name)
            redis_pipeline.hset(redis_hash_key, key, term_counter.get_count(key))

        redis_pipeline.execute()

    def _flush_all(self):
        self._redis.flushall()


if __name__ == '__main__':
    my_index = Index(make())
    term_counter = TermCounter('https://en.wikipedia.org/wiki/Cycle_detection')
    paragraphs = WikiFetcher().fetch('https://en.wikipedia.org/wiki/Cycle_detection')
    print(paragraphs)
    term_counter.process_paragraphs(paragraphs)
    # my_index.process_term_counter(term_counter)
