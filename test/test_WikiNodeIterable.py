from unittest import TestCase

import bs4
import bs4.element

from WikiNodeIterable import WikiNodeIterable
from bs4 import BeautifulSoup


class TestWikiNodeIterable(TestCase):

    def test_iter(self):
        html_paragraph1 = '<p><b>Python</b> is an <a href="/wiki/Interpreted_language" class="mw-redirect" title="Interpreted language">' \
                     'interpreted</a> <a href="/wiki/High-level_programming_language" title="High-level programming language">high-level</a> ' \
                     '<a href="/wiki/General-purpose_programming_language" title="General-purpose programming language">general-purpose programming language</a>. ' \
                     'Its design philosophy emphasizes <a href="/wiki/Code_readability" class="mw-redirect" title="Code readability">code readability</a> with its use of ' \
                     '<a href="/wiki/Off-side_rule" title="Off-side rule">significant indentation</a>. Its <a href="/wiki/Language_construct" title="Language construct">language constructs</a> ' \
                     'as well as its <a href="/wiki/Object-oriented_programming" title="Object-oriented programming">object-oriented</a> approach aim to help <a href="/wiki/Programmers" class="mw-redirect" ' \
                     'title="Programmers">programmers</a> write clear, logical code for small and large-scale projects.<sup id="cite_ref-AutoNT-7_30-0" class="reference"><a href="#cite_note-AutoNT-7-30">&#91;30&#93;</a></sup></p>'

        actual_paragraph1 = 'Python is an interpreted high-level general-purpose programming language. Its design philosophy emphasizes code readability with its use of significant indentation. Its language constructs as well as ' \
                           'its object-oriented approach aim to help programmers write clear, logical code for small and large-scale projects.[30]'

        beautiful_paragraph1 = BeautifulSoup(html_paragraph1, 'html.parser')
        iterable1 = WikiNodeIterable(beautiful_paragraph1)
        string_paragraph1 = ''
        for node in iterable1:
            if type(node) == bs4.element.NavigableString:
                string_paragraph1 += node
        string_paragraph_array1 = string_paragraph1.split(" ")
        actual_string_array1 = actual_paragraph1.split(" ")
        self.assertEqual(string_paragraph_array1, actual_string_array1)

        html_paragraph2 = '<p>Python is <a href="/wiki/Type_system#DYNAMIC" title="Type system">dynamically-typed</a> and <a href="/wiki/Garbage_collection_(computer_science)" title="Garbage collection (computer science)">garbage-collected</a>. ' \
                          'It supports multiple <a href="/wiki/Programming_paradigm" title="Programming paradigm">programming paradigms</a>, including <a href="/wiki/Structured_programming" title="Structured programming">structured</a> (particularly, <a href="/wiki/Procedural_programming" title="Procedural programming">' \
                          'procedural</a>), object-oriented and <a href="/wiki/Functional_programming" title="Functional programming">functional programming</a>. It is often described as a "batteries included" language due to its comprehensive <a href="/wiki/Standard_library" title="Standard library">standard library</a>.<sup id="cite_ref-About_31-0" class="reference"><a href="#cite_note-About-31">&#91;31&#93;</a></sup><sup id="cite_ref-32" class="reference"><a href="#cite_note-32">&#91;32&#93;</a></sup></p>'

        actual_paragraph2 = 'Python is dynamically-typed and garbage-collected. It supports multiple programming paradigms, including structured (particularly, procedural), object-oriented and functional programming. It is often described as a "batteries included" language due to its comprehensive standard library.[31][32]'

        beautiful_paragraph2 = BeautifulSoup(html_paragraph2, 'html.parser')
        iterable2 = WikiNodeIterable(beautiful_paragraph2)
        string_paragraph2 = ''
        for node in iterable2:
            if type(node) == bs4.element.NavigableString:
                string_paragraph2 += node
        string_paragraph_array2 = string_paragraph2.split(" ")
        actual_string_array2 = actual_paragraph2.split(" ")
        self.assertEqual(string_paragraph_array2, actual_string_array2)