import sys
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# print(os.path.join(os.path.dirname(__file__), '../'))
#
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

import logging

from configuration.logger import stream_handler, file_handler

from flask import Flask, request
from flask_cors import CORS
from core.sounds import find_cough_sound_prop, find_breathing_sound_prop, find_vowel_sound_prop, find_speech_sound_prop, \
    find_snoring_sound_prop

app = Flask(__name__)  # create an app instance
CORS(app)


@app.route("/", methods=["GET", "POST"])  # at the end point /
def test_run():
    app.logger.info('start test run')
    path_ref = "../test/sample.wav"
    path = os.path.join(os.path.dirname(__file__), path_ref)
    app.logger.info("Obtained file, sending the data for segmentation.")

    return find_cough_sound_prop(path, remove_noise=True, is_file=True)


@app.route("/cough", methods=["GET", "POST"])  # at the end point /
def get_cough_data():
    # print(request.files)
    # path = "../../segmentcough-master/segmentcough-master/temp.wav"
    # path = "../../segmentcough-master/segmentcough-master/snore.wav"
    data_file = request.files['audio']
    app.logger.info("Obtained file, sending the data for segmentation.")
    # data_file.save(path)
    # output = find_breathing_sound_prop(path)
    output = find_cough_sound_prop(data_file.read())
    # data_file.seek(0)
    return output


@app.route("/breath", methods=["GET", "POST"])  # at the end point /
def get_breath_data():
    # path = "../../segmentcough-master/segmentcough-master/breath.wav"
    data_file = request.files['audio']
    # app.logger.info("Obtained file, sending the data for segmentation.")
    # sound_logger.info("Obtained file, sending the data for segmentation.")

    output = find_breathing_sound_prop(data_file.read())
    app.logger.info(f'output obtained for cough sound {output}')
    # sound_logger.info(f'output obtained for cough sound {output}')
    # data_file.save(path)
    # data_file.seek(0)

    return output


@app.route("/vowel", methods=["GET", "POST"])  # at the end point /
def get_vowel_data():
    # path = "../../segmentcough-master/segmentcough-master/vowel.wav"
    data_file = request.files['audio']
    # data_file.save(path)
    # data_file.seek(0)

    return find_vowel_sound_prop(data_file.read())


@app.route("/speech", methods=["GET", "POST"])  # at the end point /
def get_speech_data():
    # path = "../../segmentcough-master/segmentcough-master/speech.wav"
    data_file = request.files['audio']
    # data_file.save(path)
    # data_file.seek(0)

    return find_speech_sound_prop(data_file.read())


@app.route("/snore", methods=["GET", "POST"])  # at the end point /
def get_snore_data():
    # path = "../../segmentcough-master/segmentcough-master/snore.wav"
    data_file = request.files['audio']
    # data_file.save(path)
    # data_file.seek(0)

    return find_snoring_sound_prop(data_file.read())


if __name__ == '__main__':
    app.logger.setLevel(logging.DEBUG)
    app.logger.addHandler(stream_handler)
    app.logger.addHandler(file_handler)

    # app.run(host="0.0.0.0", port=80, debug=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
    # app.run(host="127.0.0.1", port=5000, debug=True)
