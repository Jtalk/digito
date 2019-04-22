import os

from flask import Flask, request, redirect
from flask_cors import CORS, cross_origin

import recognition

UI_LOCATION = os.environ['UI_ADDRESS']

app = Flask(__name__)
cors = CORS(app)


@app.route('/')
def index():
    return redirect(UI_LOCATION)


@app.route('/recognise', methods=['POST'])
@cross_origin(origins=UI_LOCATION)
def recognise():
    img_raw = request.files['image']
    img_binary = img_raw.read()
    digit = recognition.recognise(img_binary)
    return str(digit)


@app.cli.command()
def prepare():
    recognition.prepare()
    print('The model is successfully trained')
