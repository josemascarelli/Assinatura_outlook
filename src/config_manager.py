import configparser
import os


class ConfigParser():
    def __init__(self):
        self.file = 'config.ini'
        # Verifica se o arquivo de configuração já existe
        if not os.path.exists(self.file):
            # Cria um novo arquivo de configuração:
            config = configparser.ConfigParser()
            config.add_section('LDAP')
            config.set('LDAP', 'server', 'ldap://domain.com')
            config.set('LDAP', 'username', 'user@domain')
            config.set('LDAP', 'password', 'password')
            config.set('LDAP', 'searchbase', 'dc=domain,dc=com')
            config.set('LDAP', 'searchfilter', '(&(objectCategory=person)(objectClass=user)(sAMAccountName={current_user}))')
            config.set('LDAP', 'attributes', 'displayName, mail, telephoneNumber, streetAddress, postalCode')

            config.add_section('Signature')
            config.set('Signature', 'templatedir', '.')
            config.set('Signature', 'templatefile', 'signature_template.html')
            config.set('Signature', 'signaturefile', 'assinatura.htm')
                
            config.add_section('URL')
            config.set('URL', 'image01', 'https://example.com/image01.jpg')
            config.set('URL', 'image02', 'https://example.com/image02.jpg')
            config.set('URL', 'image03', 'https://example.com/image03.jpg')
            # Cria um novo arquivo de configuração
            with open(self.file, 'w') as file:
                config.write(file)
                print(f'Created {self.file} successfully.')

        self.config = configparser.ConfigParser()
        self.config.read(self.file)
    
    def get(self, section, option):
        value = self.config.get(section, option)
        return value
        


