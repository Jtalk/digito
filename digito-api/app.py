import logconf
import logging
import os

from flask_cors import CORS, cross_origin
from flask import Flask, request, redirect

from client import TensorflowClient
from recognition import Recognition

UI_LOCATION = os.getenv('UI_LOCATION', 'http://localhost:3000').split(',')
TF_SERVING_LOCATION = os.getenv('TENSORFLOW_LOCATION', 'http://localhost:8501')

app = Flask(__name__)
cors = CORS(app)
log = logging.getLogger('app')

log.info('Starting app...')
recognition = Recognition(TensorflowClient(TF_SERVING_LOCATION + "/v1"))


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
    return 'OK'


@app.route('/readiness')
def readiness():
    recognition.check()
    return 'OK'
