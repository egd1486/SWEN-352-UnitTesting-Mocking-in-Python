import unittest
from unittest.mock import Mock, MagicMock
from library import library_db_interface, patron

class TestLibbraryDBInterface(unittest.TestCase):

    def setUp(self):
        self.db_interface = library_db_interface.Library_DB()

    def tearDown(self):
        self.db_interface.close_db()

    def test_insert_patron_not_in_db(self):
        patron_mock = Mock()
        self.db_interface.retrieve_patron = Mock(return_value=None)
        data = {'fname': 'name', 'lname': 'name', 'age': '2', 'memberID': '3',
                'borrowed_books': []}
        self.db_interface.convert_patron_to_db_format = Mock(return_value=data)
        self.db_interface.db.insert = Mock(side_effect=lambda x: 10 if x==data else 0)
        self.assertEqual(self.db_interface.insert_patron(patron_mock), 10)

    def test_insert_patron_already_in_db(self):
        patron_mock = Mock()
        self.db_interface.retrieve_patron = Mock(return_value=patron_mock)
        self.assertIsNone(self.db_interface.insert_patron(patron_mock))

    def test_insert_patron_false_patron(self):
        patron_mock = MagicMock()
        # Does a check to see if the patron is None or False, can't set __bool__ to none
        # If patron is none or false returns none, so asserting that
        patron_mock.__bool__.return_value = False
        self.assertIsNone(self.db_interface.insert_patron(patron_mock))

    def test_get_patron_count(self):
        results_mock = MagicMock()
        # get patron count returns lenght of results,
        # so just setting length and mocking the "all" call that
        # then has len() called on the results of
        results_mock.__len__.return_value = 10
        self.db_interface.db.all = Mock(return_value=results_mock)
        self.assertEqual(self.db_interface.get_patron_count(), 10)

    def test_get_all_patrons(self):
        patron_mock = Mock()
        # mocking the outside api call that grabs patrons,
        # makes sure that the get_all_patrons returns what the api returns
        self.db_interface.db.all = Mock(return_value=[patron_mock])        
        self.assertEqual(self.db_interface.get_all_patrons(), [patron_mock])

    def test_update_patron(self):
        data = {'fname': 'name', 'lname': 'name', 'age': '2', 'memberID': '3',
                'borrowed_books': []}
        self.db_interface.convert_patron_to_db_format = Mock(return_value=data)
        db_update_mock = Mock()
        self.db_interface.db.update = db_update_mock
        self.db_interface.update_patron(Mock())
        db_update_mock.assert_called()

    def test_update_patron_false(self):
        patron_mock = MagicMock()
        # making sure that if given false or None patron
        # that None is returned by check
        patron_mock.__bool__.return_value = False
        self.assertIsNone(self.db_interface.update_patron(patron_mock))

    def test_retrieve_patron_data_compare(self):
        # retrieving a patron and making sure the data is the same
        data = [{'fname': 'name', 'lname': 'name', 'age': '2', 'memberID': '3',
                'borrowed_books': []}]
        self.db_interface.db.search = Mock(return_value=data)
        mock_member_id = Mock()
        retrieved: patron.Patron = self.db_interface.retrieve_patron(mock_member_id)


        self.assertEqual(retrieved.fname, data[0]['fname'])
        self.assertEqual(retrieved.lname, data[0]['lname'])
        self.assertEqual(retrieved.age, data[0]['age'])
        self.assertEqual(retrieved.memberID, data[0]['memberID'])
        self.assertEqual(retrieved.borrowed_books, data[0]['borrowed_books'])

    def test_retrieve_patron_object_compare(self):
        # retreiving a patron and making sure that
        # the data is the same when __eq__ is called
        # thereby checking __dict__ of patrons
        # effectively makes sure patron is constructed properly
        data = [{'fname': 'name', 'lname': 'name', 'age': '2', 'memberID': '3',
                'borrowed_books': []}]
        self.db_interface.db.search = Mock(return_value=data)
        mock_member_id = Mock()
        retrieved: patron.Patron = self.db_interface.retrieve_patron(mock_member_id)

        mock_patron = Mock()
        mock_patron.__dict__ = {'fname': 'name', 'lname': 'name', 'age': '2', 'memberID': '3',
                'borrowed_books': []}
        
        self.assertEqual(retrieved, mock_patron)



    def test_retrieve_patron_false(self):
        # Making sure that if search returns False / None
        # this returns None
        self.db_interface.db.search = Mock(return_value=False)
        self.assertIsNone(self.db_interface.retrieve_patron(Mock()))

    def test_convert_patron_to_db_format(self):
        patron_mock = Mock()

        patron_mock.get_fname = Mock(return_value=1)
        patron_mock.get_lname = Mock(return_value=2)
        patron_mock.get_age = Mock(return_value=3)
        patron_mock.get_memberID = Mock(return_value=4)
        patron_mock.get_borrowed_books = Mock(return_value=5)
        self.assertEqual(self.db_interface.convert_patron_to_db_format(patron_mock),
                         {'fname': 1, 'lname': 2, 'age': 3, 'memberID': 4,
                          'borrowed_books': 5})