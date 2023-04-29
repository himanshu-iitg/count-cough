import json
import noisereduce as nr

import librosa
import io
import soundfile as sf
from scipy.io import wavfile
import ffmpeg
import os
from werkzeug.utils import secure_filename


def fix_riff_header(binary):
    process = (ffmpeg
               .input('pipe:0')
               .output('pipe:1', format='wav')
               .run_async(pipe_stdin=True, pipe_stdout=True, pipe_stderr=True, quiet=True, overwrite_output=True)
               )
    output, err = process.communicate(input=binary)

    riff_chunk_size = len(output) - 8
    # Break up the chunk size into four bytes, held in b.
    q = riff_chunk_size
    b = []
    for i in range(4):
        q, r = divmod(q, 256)
        b.append(r)

        # Replace bytes 4:8 in proc.stdout with the actual size of the RIFF chunk.
    riff = output[:4] + bytes(b) + output[8:]
    return riff

import pickle
import sys
import base64

from flask import Flask, request
from flask_cors import CORS
# import flask
# from scipy.io import wavfile

import os

from ops.detection import classify_cough
from ops.segmentation import segment_cough

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
    # data = request.get_data().decode()
    data = request.files['audio']
    print()
    # data = request.files['data']
    # data = request.get_json()
    # print('data', list(request.files['audio'].stream))
    # decode_string = base64.b64decode(data)
    # audio.write(decode_string)
    # audio.write(data)
    # audio.close()
    # print(decode_string.filename)
    # clip = moviepy.VideoFileClip(path)
    # clip.write_audiofile(path2)

    data.save(path)
    data.seek(0)
    # return request.get_json()
    riff = fix_riff_header(data.read())
    data, samplerate = sf.read(io.BytesIO(riff))
    # data, samplerate = sf.read(open(path, encoding='utf8', errors='ignore'))

    # fio = io.BytesIO()
    sf.write(
        path,
        data,
        samplerate=samplerate,
        subtype='PCM_16',
        format='wav'
    )
    # data = fio.getvalue()
    # print(data)
    # return segregate_cough(path)
    # return segregate_cough(data.read())
    return segregate_cough(riff)
    # return segregate_cough(data)
    # return segregate_cough(fio)
    # return {"out":"Hello World!"}         # which returns "hello world"

def segregate_cough(path):
    """
    --> detects if cough is present in the voice or not
    :param input_path:
    :return:
    """
    # fs, x = wavfile.read(path)
    # with open(path, encoding='utf8', errors='ignore') as o:
    #     fs, x = wavfile.read(o)
    # prob = cough_probability(fs, x)
    # print('prob', prob)

    # x, fs = librosa.load(path=path, sr=None, mono=True)
    x, fs = sf.read(io.BytesIO(path))

    reduced_noise = nr.reduce_noise(y=x, sr=fs)

    prob2 = cough_probability(fs, reduced_noise)
    print('prob', prob2)


    if prob2 > 0.5:
        cough_segments, mask = segment_cough(x, fs, min_cough_len=0.1)
    else:
        cough_segments = []
    # return {'segments': [s.tolist() for s in cough_segments], 'mask': mask.tolist()}
    return json.dumps({'prob2': str(prob2), 'segments': len(cough_segments)})
    # return json.dumps({'prob': str(prob), 'prob2': str(prob2), 'segments': len(cough_segments)})


def cough_probability(fs, x):
    """
    --> detects if cough is present in the voice or not
    :param input_path:
    :return:
    """
    prob = classify_cough(x, fs, model, scaler)
    return prob


if __name__ == '__main__':
   app.run(debug = True)