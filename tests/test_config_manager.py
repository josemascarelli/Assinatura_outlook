import unittest
import os
from src.config_manager import ConfigParser



class TestConfigParser(unittest.TestCase):
    
    def setUp(self):
        self.config = ConfigParser()
                
    # Check if Configuration file has been created successfully
    def test_config_file_exists(self):
        self.assertTrue(os.path.exists(self.config.file))
        
    # Check the LDAP settings have been properly configured
    def test_ldap_settings(self):
        server = self.config.get('LDAP', 'server')
        username = self.config.get('LDAP', 'username')
        password = self.config.get('LDAP', 'password')
        search_base = self.config.get('LDAP', 'searchbase')
        search_filter = self.config.get('LDAP', 'searchfilter')
        attributes = self.config.get('LDAP', 'attributes').split(',')
        
        self.assertEqual(server, 'ldap://domain.com')
        self.assertEqual(username, 'user@domain')
        self.assertEqual(password, 'password') 
        self.assertEqual(search_base, 'dc=domain,dc=com')
        self.assertEqual(search_filter, '(&(objectCategory=person)(objectClass=user)(sAMAccountName={user}))')
        self.assertCountEqual(attributes, ['displayName', 'mail', 'telephoneNumber', 'streetAddress', 'postalCode'])
        
    # Check the Signiture settings have been properly configured
    def test_signature_settings(self):
        template_dir = self.config.get('Signature', 'templatedir')
        template_file = self.config.get('Signature', 'templatefile')
        signature_file = self.config.get('Signature', 'signaturefile')

        self.assertEqual(template_dir, '.')
        self.assertEqual(template_file, 'signature_template.html')
        self.assertEqual(signature_file, 'assinatura.htm')

    # Check the URLs have been properly configured
    def test_url_settings(self):
        image01 = self.config.get('URL', 'image01')
        image02 = self.config.get('URL', 'image02')
        image03 = self.config.get('URL', 'image03')

        self.assertEqual(image01, 'https://example.com/image01.jpg')
        self.assertEqual(image02, 'https://example.com/image02.jpg')
        self.assertEqual(image03, 'https://example.com/image03.jpg')

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
