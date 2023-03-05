import configparser
import os


# Define a ConfigParser class to handle configuration file settings
class ConfigParser():
    def __init__(self):
        # Define path to configuration file
        self.file = 'config.ini'
        # Check if configuration file exists, if not create it.
        if not os.path.exists(self.file):
            # Create a new configuration file:
            config = configparser.ConfigParser()
            config.add_section('LDAP')
            config.set('LDAP', 'server', 'ldap://domain.com')
            config.set('LDAP', 'username', 'user@domain')
            config.set('LDAP', 'password', 'password')
            config.set('LDAP', 'searchbase', 'dc=domain,dc=com')
            config.set('LDAP', 'searchfilter', '(&(objectCategory=person)(objectClass=user)(sAMAccountName={user}))')
            config.set('LDAP', 'attributes', 'displayName, mail, telephoneNumber, streetAddress, postalCode')
            
            # Add Signature section and settings
            config.add_section('Signature')
            config.set('Signature', 'templatedir', '.')
            config.set('Signature', 'templatefile', 'signature_template.html')
            config.set('Signature', 'signaturefile', 'assinatura.htm')
                
            # Add URL section and settings
            config.add_section('URL')
            config.set('URL', 'image01', 'https://example.com/image01.jpg')
            config.set('URL', 'image02', 'https://example.com/image02.jpg')
            config.set('URL', 'image03', 'https://example.com/image03.jpg')
            # Write configuration file
            with open(self.file, 'w') as file:
                config.write(file)
                print(f'Created {self.file} successfully.')
        
        # Initialize ConfigParser object and read configuration from file
        self.config = configparser.ConfigParser()
        self.config.read(self.file)
        
    # Function to get configuration setting value
    def get(self, section, option):
        value = self.config.get(section, option)
        return value