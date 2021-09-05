import logconf
import recognition
import logging
import os

from flask_cors import CORS, cross_origin
from flask import Flask, request, redirect

UI_LOCATION = os.getenv('UI_LOCATION', 'http://localhost:3000').split(',')

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
