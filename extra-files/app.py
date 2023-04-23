# import librosa
import pickle
from flask import Flask, request
from flask_cors import CORS
# import flask
# from scipy.io import wavfile

# from ops.detection import classify_cough
# from ops.segmentation import segment_cough

import os


BASE_PATH = os.path.dirname(os.path.abspath(__file__))
COUGH_MODEL = os.path.join(BASE_PATH, 'models/cough_classifier')
COUGH_MODEL_SCALAR = os.path.join(BASE_PATH, 'models/cough_classification_scaler')

# with open(COUGH_MODEL, 'rb') as f:
#     model = pickle.load(f)
#
# with open(COUGH_MODEL_SCALAR, 'rb') as f:
#     scaler = pickle.load(f)

app = Flask(__name__)             # create an app instance
CORS(app)

@app.route("/",  methods=["POST"])                   # at the end point /
def hello():
    # call method hello
    return request.get_json()
    # return {"out":"Hello World!"}         # which returns "hello world"

def is_cough(fs, x):
    """
    --> detects if cough is present in the voice or not
    :param input_path:
    :return:
    """
    prob = classify_cough(x, fs, model, scaler)
    return f'The probability of cough being present in the audio is {prob}'

def segregate_cough(x, fs):
    """
    --> detects if cough is present in the voice or not
    :param input_path:
    :return:
    """
    cough_segments, mask = segment_cough(x, fs)
    # return {'segments': [s.tolist() for s in cough_segments], 'mask': mask.tolist()}
    return {'segments': len(cough_segments)}
    # return str(cough_segments)


@app.route("/prediction", methods=["GET", "POST"])
def predict():
    recieved = request.get_json()
    input_path = recieved['sound_path']
    fs, x = wavfile.read(input_path)
    if is_cough(fs, x):
        l_x, fs = librosa.load(input_path)
        return segregate_cough(l_x, fs)
    else:
        return {'segments': 0}


if __name__ == '__main__':
   app.run(debug = True)