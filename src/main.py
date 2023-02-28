import os
from configparser import ConfigParser
from getpass import getuser
from jinja2 import Environment, FileSystemLoader
from ldap3 import Server, Connection, SUBTREE, ALL_OPERATIONAL_ATTRIBUTES



class ActiveDirectory:
    def __init__(self, config: ConfigParser):
        self.config = config
        self.server = Server(self.config['LDAP']['Server'])
        self.username = self.config['LDAP']['Username']
        self.password = self.config['LDAP']['Password']
        self.search_base = self.config['LDAP']['SearchBase']
        self.search_filter = self.config['LDAP']['SearchFilter']
        self.attributes = [attr.strip() for attr in self.config['LDAP']['Attributes'].split(',')]
        self.current_user = getuser()
        # self.current_user = 'JRM' # Remover linha

    def get_user_info(self):
        with Connection(self.server, user=self.username, password=self.password) as conn:
            conn.search(
                search_base=self.search_base,
                search_filter=str(self.search_filter).format(current_user=self.current_user),
                search_scope=SUBTREE,
                attributes=self.attributes + [ALL_OPERATIONAL_ATTRIBUTES],
                paged_size=5,
            )
            if not conn.entries:
                ErrorManager.raise_error(f'User "{self.current_user}" not found on AD.')
            else:
                print(f'Found user: "{self.current_user}"')
                
            user_entry = conn.entries[0]
            user_info = {}
            for attribute in self.attributes:
                if attribute in user_entry:
                    user_info[attribute] = user_entry[attribute].value
            return user_info


class Signature:
    def __init__(self, config: ConfigParser, user_info: dict):
        self.config = config
        self.user_info = user_info
        self.template_dir = config['Signature']['TemplateDir']
        self.template_file = config['Signature']['TemplateFile']
        self.signature_file = config['Signature']['SignatureFile']
        self.template_env = Environment(loader=FileSystemLoader(self.template_dir))

    def build_signature(self):
        try:
            template = self.template_env.get_template(self.template_file)
            self.user_info.update(dict(self.config['Links']))
            return template.render(self.user_info)
        except Exception as e:
            ErrorManager.raise_error(f"Error building signature template: {e}")

    def save_signature(self):
        signature = self.build_signature()
        appdata_dir = os.getenv('APPDATA')
        signature_dir = os.path.join(appdata_dir, 'Microsoft', 'Signatures')
        if os.path.exists(signature_dir):
            signature_file = os.path.join(signature_dir, self.signature_file)
            with open(signature_file, 'w', encoding='ISO-8859-1') as f:
                try:
                    f.write(signature)
                    print(f'Added file: {signature_file}')
                except Exception as e:
                    ErrorManager.raise_error(f"Error writing signature file: {e}")
        else:
            ErrorManager.raise_error(f'Directory {signature_dir} not found')


class OutlookSignature:
    def __init__(self, config_file: str):
        self.config = ConfigParser()
        self.config.read(config_file)
        self.ad = ActiveDirectory(self.config)
        self.signature = Signature(self.config, self.ad.get_user_info())

    def run(self):
        try:
            self.signature.save_signature()
        except Exception as e:
            print(f"Error running OutlookSignature: {e}")


class ErrorManager:
    @staticmethod
    def raise_error(msg):
        raise Exception(msg)



if __name__ == '__main__':
    config_file = 'config.ini'
    outlook_sig = OutlookSignature(config_file)
    outlook_sig.run()
