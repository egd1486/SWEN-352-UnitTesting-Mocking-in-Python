import unittest
from unittest.mock import Mock
from library import library
import json

class TestLibrary(unittest.TestCase):

    def setUp(self):
        self.lib = library.Library()
        self.api = library.Books_API()
        # self.books_data = [{'title': 'Learning Python', 'ebook_count': 3}, {'title': 'Learning Python (Learning)', 'ebook_count': 1}, {'title': 'Learning Python', 'ebook_count': 1}, {'title': 'Learn to Program Using Python', 'ebook_count': 1}, {'title': 'Aprendendo Python', 'ebook_count': 1}, {'title': 'Python Basics', 'ebook_count': 1}]
        with open('tests_data/ebooks.txt', 'r') as f:
            self.books_data = json.loads(f.read())



    def test_is_ebook_true(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertTrue(self.lib.is_ebook('learning python'))

    def test_is_ebook_false(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertFalse(self.lib.is_ebook('How to Train Your Dragon'))

    def test_get_ebooks_count(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertEqual(self.lib.get_ebooks_count("learning python"), 8)

    def test_is_book_by_author_true(self):
        self.lib.api.books_by_author = Mock(return_value=["Learning Python", "Python Basics"])
        self.assertTrue(self.lib.is_book_by_author("Mark Lutz", 'Learning Python'))

    def test_is_book_by_author_false(self):
        self.lib.api.books_by_author = Mock(return_value=["Learning Python", "Python Basics"])
        self.assertFalse(self.lib.is_book_by_author("Mark Lutz", "How to Train Your Dragon"))

    def test_get_languages_for_book(self):
        self.lib.api.get_book_info = Mock(return_value=[{"title": "Learning Python", "language": ["eng"]}])

        result = self.lib.get_languages_for_book("Learning Python")

        self.assertEqual(result, {"eng"})

    def test_register_patron(self):
        self.lib.register_patron = Mock(return_value="12345")

        result = self.lib.register_patron("fname", "lname", "age", "12345")