from unittest import TestCase
from Index import Index


class RedisMock:

    __slots__ = 'data'

    def __init__(self):
        self.data = {}

    def pipeline(self):
        return self

    def delete(self, key):
        return

    def sadd(self, key, value):
        if not (key in self.data):
            self.data[key] = set()
        self.data[key].add(value)

    def hset(self, key, hash_key, value):
        if not (key in self.data):
            self.data[key] = dict()
        self.data[key][hash_key] = value

    def execute(self):
        return

    def keys(self, pattern):
        return self.data.keys()


class TermCounterMock:

    __slots__ = 'map', 'name'

    def __init__(self):
        self.name = 'https://en.wikipedia.org/wiki/Java_(programming_language)'
        self.map = {
            'java': 130,
            'python': 20,
            'tensorflow': 5,
            'springboot': 10
        }

    def get_name(self):
        return self.name

    def get_terms(self):
        return ['java', 'python', 'tensorflow', 'springboot']

    def get_count(self, term):
        return self.map[term]


class TestIndex(TestCase):

    def setUp(self) -> None:
        self.wi = Index(RedisMock())

    def tearDown(self) -> None:
        self.wi = Index(RedisMock())

    def test__redis_url_set_key(self):
        expected = "URLSet:java"
        actual = self.wi._redis_url_set_key("java")
        self.assertEqual(actual, expected)

    def test__redis_term_counter_key(self):
        expected = "TermCounter:https://en.wikipedia.org/wiki/.NET_Framework"
        actual = self.wi._redis_term_counter_key("https://en.wikipedia.org/wiki/.NET_Framework")
        self.assertEqual(actual, expected)

    def test_is_indexed(self):
        self.wi.process_term_counter(TermCounterMock())
        self.assertTrue(self.wi.is_indexed("https://en.wikipedia.org/wiki/Java_(programming_language)"))

    def test_process_term_counter(self):
        self.wi.process_term_counter(TermCounterMock())
        redis_term_key = 'TermCounter:' + 'https://en.wikipedia.org/wiki/Java_(programming_language)'
        for term in ['java', 'python', 'tensorflow', 'springboot']:
            redis_key = "URLSet:" + term
            self.assertTrue(redis_key in self.wi._redis.data)
            self.assertTrue('https://en.wikipedia.org/wiki/Java_(programming_language)' in self.wi._redis.data[redis_key])
        self.assertEqual(self.wi._redis.data[redis_term_key]['java'], 130)
        self.assertEqual(self.wi._redis.data[redis_term_key]['python'], 20)
        self.assertEqual(self.wi._redis.data[redis_term_key]['tensorflow'], 5)
        self.assertEqual(self.wi._redis.data[redis_term_key]['springboot'], 10)
