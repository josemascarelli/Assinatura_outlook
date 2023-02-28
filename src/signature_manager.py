from jinja2 import Environment, FileSystemLoader
from collections import Counter
import os

class Signature():
    def __init__(self, template_dir, template_file, user_info, image_links):
        self.template_file = template_file
        self.user_info = user_info
        self.image_links = image_links
        self.template_env = Environment(loader=FileSystemLoader(template_dir))

    def build_signature(self):
        template = self.template_env.get_template(self.template_file)
        data = dict(Counter(self.user_info) + Counter(self.image_links))
        
        return template.render(data)
    
    # def save_signature(self):
    #     signature = self.build_signature()
    #     signature_dir = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Signatures')
        