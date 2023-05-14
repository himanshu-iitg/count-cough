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

import os

from ops.detection import classify_cough
from ops.segmentation import segment_cough

# BASE_PATH = os.path.dirname(os.path.abspath(__file__))
# COUGH_MODEL = os.path.join(BASE_PATH, 'cough_models/cough_classifier')
# COUGH_MODEL_SCALAR = os.path.join(BASE_PATH, 'cough_models/cough_classification_scaler')

# with open(COUGH_MODEL, 'rb') as f:
#     model = pickle.load(f)
#
# with open(COUGH_MODEL_SCALAR, 'rb') as f:
#     scaler = pickle.load(f)

app = Flask(__name__)             # create an app instance
CORS(app)

@app.route("/",  methods=["POST"])                   # at the end point /
def hello():
    path = "temp.wav"
    # call method hello
    data_file = request.files['audio']
    # data = request.files['data']

    data_file.save(path)
    data_file.seek(0)
    # # return request.get_json()
    # data, samplerate = sf.read(io.BytesIO(data_file.read()))
    # data, samplerate = sf.read(io.BytesIO(data_file.read()))
    # data, samplerate = sf.read(open(path, encoding='utf8', errors='ignore'))

    # sf.write(
    #     path,
    #     data,
    #     samplerate=samplerate,
    #     subtype='PCM_16',
    #     format='wav'
    # )
    # data = fio.getvalue()
    return segregate_cough(data_file.read())
    # return segregate_cough(data_file)
    # return segregate_cough(path)

def segregate_cough(path):
    """
    --> detects if cough is present in the voice or not
    :param input_path:
    :return:
    """

    # x, fs = librosa.load(path=path, sr=None, mono=True)
    # x, fs = sf.read(io.BytesIO(path))
    # x, fs = sf.read(file=io.BytesIO(path).read())
    x, fs = sf.read(io.BytesIO(path), dtype=np.int16)
    # x, fs = sf.read(file=path, dtype=np.int16)
    if len(x.shape) > 1:
        x = np.mean(x, axis=1)

    # wav_data = nr.reduce_noise(y=x, sr=fs, stationary=True)
    # reduced_noise = wav_data / 32768.0
    reduced_noise = x / 32768.0

    segment, mask = segment_cough(reduced_noise, fs, min_cough_len=0.05, th_l_multiplier=0.05, th_h_multiplier=3, cough_padding=0.5)

    params = yamnet_params.Params(sample_rate=fs, patch_hop_seconds=0.1)

    class_names = yamnet_model.class_names('models/research/audioset/yamnet/yamnet_class_map.csv')
    yamnet = yamnet_model.yamnet_frames_model(params)
    yamnet.load_weights('cough_models/yamnet.h5')

    scores, embeddings, spectrogram = yamnet(reduced_noise)
    scores = scores.numpy()

    # reduced_noise = nr.reduce_noise(y=x, sr=fs, stationary=True)

    mean_prob2 = cough_probability(scores)
    print('prob', mean_prob2)

    print('len of segment', len(segment))

    count = 0
    for i, s in enumerate(segment):
        s = nr.reduce_noise(s, fs, stationary=True)
        sc, embeddings, spectrogram = yamnet(s)
        print(f'number = {i}', cough_probability(sc))
        if cough_probability(sc)>0.3:
            # sf.write(
            #     f'no_n_seg_{i}.wav',
            #     s,
            #     samplerate=fs,
            #     subtype='PCM_16',
            #     format='wav'
            # )
            count+=1

    mean_scores = np.mean(scores, axis=0)
    top_class_indices = np.argsort(mean_scores)[::-1][:TOP_N]
    yticks = range(0, TOP_N, 1)
    pprint([(top_class_indices[x], class_names[top_class_indices[x]], mean_scores[top_class_indices[x]]) for x in yticks])

    # plt.imshow(scores[:, top_class_indices].T, aspect='auto', interpolation='nearest', cmap='gray_r')
    # Compensate for the patch_window_seconds (0.96s) context window to align with spectrogram.
    # patch_padding = (params.patch_window_seconds / 2) / params.patch_hop_seconds
    # plt.xlim([-patch_padding, scores.shape[0] + patch_padding])
    # Label the top_N classes.
    # plt.yticks(yticks, [class_names[top_class_indices[x]] for x in yticks])
    # _ = plt.ylim(-0.5 + np.array([TOP_N, 0]))
    # plt.savefig('variety.png')
    # return {'segments': [s.tolist() for s in cough_segments], 'mask': mask.tolist()}
    # return json.dumps({'prob2': str(mean_prob2), 'segments': len(cough_segments)})
    print(json.dumps({'prob2': str(mean_prob2), 'segments': count}))
    return json.dumps({'prob2': str(mean_prob2), 'segments': count})
    # return json.dumps({'prob': str(prob), 'prob2': str(prob2), 'segments': len(cough_segments)})


def cough_probability(scores):
    """
    --> detects if cough is present in the voice or not
    :param input_path:
    :return:
    """
    prob = np.mean(scores[:, 42])
    # prob = np.mean(scores[:, 36])
    return prob


if __name__ == '__main__':
   app.run(debug = True)