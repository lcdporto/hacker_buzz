import os
import sys
import settings
import requests
from requests import exceptions
import shutil
import string
import random

from custom import MissingFile

def random_filename():
    pool = string.digits + string.ascii_lowercase
    return ''.join(random.SystemRandom().choice(pool) for _ in range(6)) + '.jpg'

def save_image(request):
    """
    Save image to filesystem
    """
    upload = request.files.get('image')
    if upload is None:
        raise Exception
    upload.save(settings.UPLOADS, True)
    return upload

def save_image_from_url(request):
    """
    Save image to filesystem
    """
    filename = None
    try:
        url = request.forms['url']
        response = requests.get(url, stream=True, timeout=500)
        if response.status_code == 200 and response.headers['content-type'] == 'image/jpeg':
            filename = random_filename()
            with open(os.path.join(settings.UPLOADS, filename), 'wb') as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)
    except exceptions.ConnectionError:
        sys.stdout.write("Connection problem skipping: %s   \r" % (url) )
    except exceptions.Timeout:
        sys.stdout.write("Connection timeout skipping: %s   \r" % (url) )
    except exceptions.TooManyRedirects:
        sys.stdout.write("Too many redirects skipping: %s   \r" % (url) )
    return filename
