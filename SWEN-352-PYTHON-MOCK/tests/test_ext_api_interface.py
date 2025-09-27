import unittest
from library import ext_api_interface
from unittest.mock import Mock
import requests
import json

class TestExtApiInterface(unittest.TestCase):
    def setUp(self):
        self.api = ext_api_interface.Books_API()
        self.book = "learning python"
        with open('tests_data/ebooks.txt', 'r') as f:
            self.books_data = json.loads(f.read())
        with open('tests_data/json_data.txt', 'r') as f:
            self.json_data = json.loads(f.read())

    def test_make_request_True(self):
        attr = {'json.return_value': dict()}
        requests.get = Mock(return_value = Mock(status_code = 200, **attr))
        self.assertEqual(self.api.make_request(""), dict())

    def test_make_request_connection_error(self):
        ext_api_interface.requests.get = Mock(side_effect=requests.ConnectionError)
        url = "some url"
        self.assertEqual(self.api.make_request(url), None)

    def test_make_request_False(self):
        requests.get = Mock(return_value=Mock(status_code=100))
        self.assertEqual(self.api.make_request(""), None)

    # def test_get_ebooks(self):
    #     self.api.make_request = Mock(return_value=self.json_data)
    #     self.assertEqual(self.api.get_ebooks(self.book), self.books_data)

#ABOVE FROM MOCK_HINT
# Note: 100 = continue, 200 = OK
    def test_book_available_True(self):
        """Test if existing book is available"""
        # is_book_available expects a dictionary with key 'docs' that contains list of >= 1 items
        #  defining the simulated data structure 
        mock_response_data = {'docs': [{'title': self.book}]}
        # replacing the real make_request with a mock that returns the simulated data
            # more efficient bc doesnt make real API request
        self.api.make_request = Mock(return_value=mock_response_data)
        self.assertEqual(self.api.is_book_available(self.book), True, "existing book not found")
    
    def test_book_available_False_1(self):
        """Test if non-existant book is available"""
        mock_response_data = {'docs': []}
        self.api.make_request = Mock(return_value=mock_response_data)
        self.assertEqual(self.api.is_book_available(self.book), False, "non-existant book found")
    
    def test_book_available_False_2(self):
        """Test if blank book is available"""
        mock_response_data = {'docs': []}
        self.api.make_request = Mock(return_value=mock_response_data)
        self.assertEqual(self.api.is_book_available(""), False, "blank book found")
        
    def test_book_available_False_3(self):
        """Test if book is available in non-existent library"""
        self.api.make_request = Mock(return_value=None)
        self.assertEqual(self.api.is_book_available(self.book), False, "json was not empty")
        
        
    def test_books_by_author_1(self):
        """Test getting book by author"""
        mock_response_data = {'docs': [{'title_suggest': "The Way of Mark"}]}
        self.api.make_request = Mock(return_value=mock_response_data)
        self.assertEqual(self.api.books_by_author("Mark Lutz"), ["The Way of Mark"], "book not found")
    
    def test_books_by_author_2(self):
        """Test getting books by author"""
        mock_response_data = {'docs': [{'title_suggest': "The Way of Mark"},
                                    {'title_suggest': "How to Be a Lutz"}]}
        self.api.make_request = Mock(return_value=mock_response_data)
        expected = ["The Way of Mark", "How to Be a Lutz"]
        self.assertEqual(self.api.books_by_author("Mark Lutz"), expected, "books not found")
        
    def test_books_by_author_3(self):
        """Test getting books by author in non-existent library"""
        self.api.make_request = Mock(return_value=None)
        self.assertEqual(self.api.books_by_author("Mark Lutz"), [], "books found by author")
    
    
    def test_book_info_1(self):
        """Test getting book info"""
        mock_repsonse_data = {'docs': [{'title': self.book,
                                        'publisher': 'Frank Sinatra',
                                        'publish_year': 1990,
                                        'language': 'eng'}]}
        self.api.make_request = Mock(return_value=mock_repsonse_data)
        expected = [{'title': self.book,
                    'publisher': 'Frank Sinatra',
                    'publish_year': 1990,
                    'language': 'eng'}]
        self.assertEqual(self.api.get_book_info(self.book), expected, "missing book info")
        
    def test_book_info_2(self):
        """Test getting book infos"""
        mock_repsonse_data = {'docs': [{'title': self.book,
                                        'publisher': 'Frank Sinatra',
                                        'publish_year': 1990,
                                        'language': 'eng'},
                                       {'title': self.book,
                                        'publisher': 'Mark Sinatra',
                                        'publish_year': 1990,
                                        'language': 'eng'}]}
        self.api.make_request = Mock(return_value=mock_repsonse_data)
        expected = [{'title': self.book,
                    'publisher': 'Frank Sinatra',
                    'publish_year': 1990,
                    'language': 'eng'},
                    {'title': self.book,
                    'publisher': 'Mark Sinatra',
                    'publish_year': 1990,
                    'language': 'eng'}]
        self.assertEqual(self.api.get_book_info(self.book), expected, "wrong book infos")
        
    def test_book_info_3(self):
        """Test getting minimal book info"""
        mock_repsonse_data = {'docs': [{'title': self.book}]}
        self.api.make_request = Mock(return_value=mock_repsonse_data)
        expected = [{'title': self.book}]
        self.assertEqual(self.api.get_book_info(self.book), expected, "have all book info")
        
    def test_book_info_4(self):
        """Test getting book info from non-existent library"""
        self.api.make_request = Mock(return_value=None)
        self.assertEqual(self.api.get_book_info(self.book), [], "book info found")
    
    
    def test_ebooks_1(self):
        """Test get ebooks"""
        mock_repsonse_data = {'docs': [{'ebook_count_i': 1,
                                        'title': self.book}]}
        self.api.make_request = Mock(return_value=mock_repsonse_data)
        expected = [{'title': self.book,
                     'ebook_count': 1}]
        self.assertEqual(self.api.get_ebooks(self.book), expected, "ebooks not found")
        
    def test_ebooks_2(self):
        """Test get no ebooks"""
        mock_repsonse_data = {'docs': [{'ebook_count_i': 0,
                                        'title': self.book}]}
        self.api.make_request = Mock(return_value=mock_repsonse_data)
        self.assertEqual(self.api.get_ebooks(self.book), [], "found ebooks")
    
    def test_ebooks_3(self):
        """Test get ebooks in non-existent library"""
        self.api.make_request = Mock(return_value=None)
        self.assertEqual(self.api.get_ebooks(self.book), [], "found ebooks in non-existent library")
    
    