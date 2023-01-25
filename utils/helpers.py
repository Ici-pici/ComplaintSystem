import base64
import re

from werkzeug.exceptions import BadRequest

models = ['ApproverModel', 'ComplainerModel', 'AdminModel']

def decode_photo(path, encoded_photo):
    with open(path, 'wb') as file:
        try:
            file.write(base64.b64decode(encoded_photo.encode('utf-8')))
        except Exception:
            raise BadRequest('Photo decoding failed')

def get_file_name_from_url(url):
    regex = r'//.*/(?P<file_name>.*)'
    results = re.findall(regex, url)
    return results[0]
