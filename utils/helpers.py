import base64
from werkzeug.exceptions import BadRequest

def decode_photo(path, encoded_photo):
    with open(path, 'wb') as file:
        try:
            file.write(base64.b64decode(encoded_photo.encode('utf-8')))
        except Exception:
            raise BadRequest('Photo decoding failed')
