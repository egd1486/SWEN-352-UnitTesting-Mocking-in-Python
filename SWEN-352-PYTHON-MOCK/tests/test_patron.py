import unittest
from library import patron

class TestPatron(unittest.TestCase):

    def setUp(self):
        self.pat = patron.Patron('fname', 'lname', '20', '1234')

    def test_valid_name(self):
        pat = patron.Patron('fname', 'lname', '20', '1234')
        self.assertTrue(isinstance(pat, patron.Patron))

    def test_invalid_name(self):
        self.assertRaises(patron.InvalidNameException, patron.Patron, '1fname', '1lname', '20', '1234')
    
    #Attempts to borrow the same book twice
    #Verifies the book was only added once
    def test_add_borrowed_book_fail(self):
        self.pat.add_borrowed_book('Book1')
        self.pat.add_borrowed_book('Book1')
        self.assertEqual(len(self.pat.get_borrowed_books()), 1)
    
    #Tests to make sure that two patrons with different info are not equal
    def test_not_equal(self):
        pat2 = patron.Patron('Jimmy', 'Bob', '93', '1235')
        self.assertNotEqual(self.pat, pat2)
        