from unittest import TestCase
from TermCounter import TermCounter


class TestTermCounter(TestCase):

    def setUp(self) -> None:
        self.tc_name = 'Python_(programming_language)'
        self.tc = TermCounter(self.tc_name)

    def tearDown(self) -> None:
        self.tc = TermCounter(self.tc_name)

    def test_get_name(self):
        self.assertEqual(self.tc.get_name(), self.tc_name)

    def test__increment_count(self):
        self.assertEqual(self.tc.get_count('hello'), 0)
        self.tc._increment_count('hello')
        self.assertEqual(self.tc.get_count('hello'), 1)
        for i in range(10):
            self.tc._increment_count('world')
        self.assertEqual(self.tc.get_count('world'), 10)

    def test_get_count(self):
        self.assertEqual(self.tc.get_count('world'), 0)
        for i in range(10):
            self.tc._increment_count('world')
        self.assertEqual(self.tc.get_count('world'), 10)

    def test_get_terms(self):
        terms = ['hello', 'world', 'foo', 'bar']
        for t in terms:
            self.tc._increment_count(t)
        self.assertEqual(terms, self.tc.get_terms())

    def test_has_term(self):
        self.assertFalse(self.tc.has_term('world'))
        self.tc._increment_count('foo')
        self.assertTrue(self.tc.has_term('foo'))

    def test_remove_punctuation_and_text_from_text(self):
        actual = self.tc.remove_punctuation_and_text_from_text("n165[s]+='hello.<%@WORLD'Foo")
        expected = "ns'helloworld'foo"
        self.assertEqual(actual, expected)
