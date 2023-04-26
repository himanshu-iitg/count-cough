import librosa
import io
import soundfile as sf
# import moviepy.editor as moviepy
# from six.moves.urllib.request import urlopen
from werkzeug.utils import secure_filename

import pickle
import sys
import base64

from flask import Flask, request
from flask_cors import CORS
# import flask
# from scipy.io import wavfile

# from ops.detection import classify_cough
# from ops.segmentation import segment_cough

import os

from ops.detection import classify_cough

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
COUGH_MODEL = os.path.join(BASE_PATH, 'models/cough_classifier')
COUGH_MODEL_SCALAR = os.path.join(BASE_PATH, 'models/cough_classification_scaler')

with open(COUGH_MODEL, 'rb') as f:
    model = pickle.load(f)

with open(COUGH_MODEL_SCALAR, 'rb') as f:
    scaler = pickle.load(f)

app = Flask(__name__)             # create an app instance
CORS(app)

@app.route("/",  methods=["POST"])                   # at the end point /
def hello():
    path = "temp.wav"
    # path2 = "out_audio.wav"
    # audio = open(path, "wb")
    # call method hello
    # app.logger.info(request.get_json())
    # print(request, file=sys.stderr)
    # data = request.get_data()
    data = request.files['audio']
    # data = request.files['data']
    # data = request.get_json()
    print('data', request.files['audio'])
    # decode_string = base64.b64decode(data)
    # audio.write(decode_string)
    # audio.write(data)
    # audio.close()
    # print(decode_string.filename)
    # clip = moviepy.VideoFileClip(path)
    # clip.write_audiofile(path2)

    data.save(path)
    data.seek(0)
    x, fs = librosa.load(path=path, sr=None, mono=True)
    # x, fs = sf.read(data.stream)
    # x, fs = sf.read(data)
    # with open(data, 'rb') as f:
        # print('request printed', f)
    # print('request printed', request.get_data().decode("utf-8"))
    # return request.get_json()
    return is_cough(fs, x)
    # return {"out":"Hello World!"}         # which returns "hello world"

def is_cough(fs, x):
    """
    --> detects if cough is present in the voice or not
    :param input_path:
    :return:
    """
    prob = classify_cough(x, fs, model, scaler)
    return {'prob': str(round(prob, 2))}


if __name__ == '__main__':
   app.run(debug = True)