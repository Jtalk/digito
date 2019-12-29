import logconf

logconf.init_logs()

import os
import logging

from flask import Flask, request, redirect
from flask_cors import CORS, cross_origin

import recognition

UI_LOCATION = os.environ['UI_LOCATION'].split(',')

app = Flask(__name__)
cors = CORS(app)
log = logging.getLogger('app')

print('Starting app...')

@app.route('/')
def index():
    return redirect(UI_LOCATION[0])


@app.route('/recognise', methods=['POST'])
@cross_origin(origins=UI_LOCATION)
def recognise():
    log.info('Image recognition request was received')
    img_raw = request.files['image']
    img_binary = img_raw.read()
    log.debug('Successfully retrieved the file, recognising')
    digit = recognition.recognise(img_binary)
    return str(digit)


@app.route('/health')
def health():
    recognition.check()
    return 'OK'
