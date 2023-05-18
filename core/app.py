import json
from pprint import pprint

import noisereduce as nr

import sys

import matplotlib.pyplot as plt

sys.path.append('models/research/audioset/yamnet')

import params as yamnet_params
import yamnet as yamnet_model
import tensorflow as tf

import numpy as np
import io
import soundfile as sf

import pickle

from flask import Flask, request
from flask_cors import CORS

TOP_N = 5

app = Flask(__name__)             # create an app instance
CORS(app)

@app.route("/cough",  methods=["POST"])                   # at the end point /
def hello():
    # path = "temp.wav"
    data_file = request.files['audio']

    # data_file.save(path)
    # data_file.seek(0)

    return segregate_cough(data_file.read())

if __name__ == '__main__':
   app.run(debug = True)