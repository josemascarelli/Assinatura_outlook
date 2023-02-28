import os
from configparser import ConfigParser
from getpass import getuser
from jinja2 import Environment, FileSystemLoader
from ldap_manager import ActiveDirectory



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
        self.ad = ActiveDirectory()
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
