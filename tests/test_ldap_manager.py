import unittest
from unittest.mock import patch
from src.ldap_manager import ActiveDirectory



class TestActiveDirectory(unittest.TestCase):

    def setUp(self):
        # Set up a default instance of ActiveDirectory for testing purposes.
        self.ad = ActiveDirectory(server="test.server.com", username="test_username", password="test_password", search_base="dc=test,dc=com")
    
    @patch('active_directory.Connection.bind')
    @patch('active_directory.Connection.search')
    def test_get_user_attr(self, mock_search, mock_bind):
        
        # Case 1: when search returns no entries
        mock_search.return_value.entries = []
        result = self.ad.get_user_attr("joe", attributes=['cn', 'uid'])
        self.assertEqual(result, {})
        
        # Case 2: when search returns more than one entry
        mock_search.return_value.entries = [1,2]
        with self.assertRaises(ValueError) as context:
            self.ad.get_user_attr("joe", attributes=['cn', 'uid'])
        self.assertTrue("Multiple entries found" in str(context.exception))

        # Case 3: when attributes not found on the user entry
        mock_search.return_value.entries = [{"uid": ['1234']}]
        result = self.ad.get_user_attr("joe", attributes=["displayName"])
        self.assertEqual(result, {})

        # Case 4: when a correct attribute list is provided, and search is successful
        mock_search.return_value.entries = [{"uid": ['1234'], "cn":["Joe"], "displayName":["Joe Smith"]}]
        result = self.ad.get_user_attr("joe", attributes=["cn", "uid", "displayName"])
        self.assertEqual(result, {"uid":['1234'], "cn":["Joe"], "displayName":["Joe Smith"]})

    @patch('active_directory.Connection.bind')
    def test_bind_exception(self, mock_bind):
        # Case 5: test Bind function throws an exception
        mock_bind.side_effect = Exception("Error Binding to LDAP server")
        with self.assertRaises(ValueError) as context:
            self.ad.get_user_attr("joe", attributes=['cn', 'uid'])
        self.assertTrue("User test_username was not able to bind" in str(context.exception))


if __name__ == '__main__':
    unittest.main()
