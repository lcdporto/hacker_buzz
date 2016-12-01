#!/usr/bin/env python
import bottle
import subprocess
import os
import classifier
import settings
import utils

from custom import MissingFile

p1 = subprocess.Popen(['ip','addr','show','eth0'],stdout=subprocess.PIPE)
p2 = subprocess.Popen(['sed','-rn',r's/\s*inet\s(([0-9]{1,3}\.){3}[0-9]{1,3}).*/\1/p'],stdin=p1.stdout,stdout=subprocess.PIPE)
p1.stdout.close()
ip_addr = p2.communicate()[0].strip()
p1.wait()

app = bottle.app()

@app.hook('after_request')
def handle_cors():
    """
    Let there be no cors at all ;)
    """
    bottle.response.headers['Access-Control-Allow-Origin'] = '*'
    bottle.response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    bottle.response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

@bottle.route('/')
def index():
    return {'status': 'ok'}

@bottle.route('/classifications', method=['OPTIONS', 'POST'])
def classify():
    if bottle.request.method == 'OPTIONS':
        return {}
    try:
        img = utils.save_image(bottle.request)
        return classifier.classify(settings.UPLOADS + img.filename)
    except MissingFile:
        return {'error': 'missing image file'}

@bottle.route('/urls', method=['OPTIONS', 'POST'])
def classify_url():
    if bottle.request.method == 'OPTIONS':
        return {}
    filename= utils.save_image_from_url(bottle.request)
    return classifier.classify(settings.UPLOADS + filename)


if __name__=='__main__':
    bottle.debug(True)
    bottle.run(app=app, host='localhost', port=80)
