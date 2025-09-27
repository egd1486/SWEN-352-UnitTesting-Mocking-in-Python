import unittest
from unittest.mock import Mock
from library import library
from library import patron
import json

class TestLibrary(unittest.TestCase):

    def setUp(self):
        self.lib = library.Library()
        self.api = library.Books_API()
        # self.books_data = [{'title': 'Learning Python', 'ebook_count': 3}, {'title': 'Learning Python (Learning)', 'ebook_count': 1}, {'title': 'Learning Python', 'ebook_count': 1}, {'title': 'Learn to Program Using Python', 'ebook_count': 1}, {'title': 'Aprendendo Python', 'ebook_count': 1}, {'title': 'Python Basics', 'ebook_count': 1}]
        with open('tests_data/ebooks.txt', 'r') as f:
            self.books_data = json.loads(f.read())

    def tearDown(self):
        self.lib.db.close_db()

    def test_is_ebook_true(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertTrue(self.lib.is_ebook('learning python'))

    #Does an assertFalse call with a book not in the mocked data
    def test_is_ebook_false(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertFalse(self.lib.is_ebook('How to Train Your Dragon'))

    def test_get_ebooks_count(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertEqual(self.lib.get_ebooks_count("learning python"), 8)

    #Does an assertTrue call with a book and author in the mocked data
    def test_is_book_by_author_true(self):
        self.lib.api.books_by_author = Mock(return_value=["Learning Python", "Python Basics"])
        self.assertTrue(self.lib.is_book_by_author("Mark Lutz", 'Learning Python'))

    #Does an assertFalse call with a book not by the given author in the mocked data
    def test_is_book_by_author_false(self):
        self.lib.api.books_by_author = Mock(return_value=["Learning Python", "Python Basics"])
        self.assertFalse(self.lib.is_book_by_author("Mark Lutz", "How to Train Your Dragon"))

    #Does an assertEqual call with a books langauge in the mocked data
    def test_get_languages_for_book(self):
        self.lib.api.get_book_info = Mock(return_value=[{"title": "Learning Python", "language": ["eng"]}])

        result = self.lib.get_languages_for_book("Learning Python")

        self.assertEqual(result, {"eng"})

    #Does multiple assertEqual calls
    #Verifies the registered info is correct
    #Asserts the db insert method was called
    def test_register_patron(self):
        self.lib.db.insert_patron = Mock(return_value=12345)
        result = self.lib.register_patron("John", "Smith", 25, 12345)
        
        self.assertEqual(result, 12345)
        
        self.lib.db.insert_patron.assert_called()
        
        patron_arg = self.lib.db.insert_patron.call_args[0][0]
        self.assertEqual(patron_arg.fname, "John")
        self.assertEqual(patron_arg.lname, "Smith")
        self.assertEqual(patron_arg.age, 25)
        self.assertEqual(patron_arg.memberID, 12345)
    
    #Does an assertTrue call to verify a patron is registered
    def test_is_patron_registered_true(self):
        registered_patron = patron.Patron("John", "Smith", 25, 12345)
        self.lib.db.retrieve_patron = Mock(return_value=Mock())
        self.assertTrue(self.lib.is_patron_registered(registered_patron))
    
    #Does an assertFalse call to verify a patron is not registered
    def test_is_patron_registered_false(self):
        registered_patron = patron.Patron("John", "Smith", 25, 12345)
        self.lib.db.retrieve_patron = Mock(return_value=None)
        self.assertFalse(self.lib.is_patron_registered(registered_patron))
    
    #Adds a book to a patron's borrowed books and verifies it was added
    #Asserts the db update method was called for the patron
    def test_borrow_book(self):
        obj_patron = patron.Patron("John", "Smith", 25, 12345)
        self.lib.db.update_patron = Mock()
        
        self.lib.borrow_book("Learning Python", obj_patron)
        
        self.assertIn("learning python", obj_patron.get_borrowed_books())
        self.lib.db.update_patron.assert_called_with(obj_patron)
    
    #Removes a book from a patron's borrowed books and verifies it was removed
    #Asserts the db update method was called for the patron   
    def test_return_book(self):
        obj_patron = patron.Patron("John", "Smith", 25, 12345)
        self.lib.borrow_book("Learning Python", obj_patron)
        self.lib.db.update_patron = Mock()
        
        self.lib.return_borrowed_book("Learning Python", obj_patron)
        
        self.assertNotIn("learning python", obj_patron.get_borrowed_books())
        self.lib.db.update_patron.assert_called_with(obj_patron)
    
    #Does an assertTrue call to verify a patron has borrowed a specific book
    def test_is_book_borrowed_true(self):
        obj_patron = patron.Patron("John", "Smith", 25, 12345)
        self.lib.borrow_book("Learning Python", obj_patron)
        self.lib.db.update_patron = Mock()
        
        self.assertTrue(self.lib.is_book_borrowed("Learning Python", obj_patron))
    
    #Does an assertFalse call to verify a patron has not borrowed a specific book
    def test_is_book_borrowed_false(self):
        obj_patron = patron.Patron("John", "Smith", 25, 12345)
        self.lib.db.update_patron = Mock()
        
        self.assertFalse(self.lib.is_book_borrowed("Learning Python", obj_patron))