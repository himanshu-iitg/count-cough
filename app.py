import sys
import os
import serverless_wsgi

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

sys.path.append(os.path.join(os.path.dirname(__file__), '/'))

import logging

from configuration.logger import stream_handler

from flask import Flask, request
from flask_cors import CORS
from core.sounds import find_cough_sound_prop, find_breathing_sound_prop, find_vowel_sound_prop, find_speech_sound_prop, \
    find_snoring_sound_prop, find_blow_sound_prop

app = Flask(__name__)  # create an app instance
CORS(app)


@app.route("/", methods=["GET", "POST"])  # at the end point /
def test_run():
    app.logger.info('start test run')
    path_ref = "test/cough.wav"#"C:\\Users\\Lenovo\\Desktop\\cough_1.wav"
    path = os.path.join(os.path.dirname(__file__), path_ref)
    app.logger.info("Obtained file, sending the data for segmentation.")

    return find_cough_sound_prop(path, remove_noise=False, is_file=True)


@app.route("/cough", methods=["GET", "POST"])  # at the end point /
def get_cough_data():
    # print(request.files)
    # path = "../../segmentcough-master/segmentcough-master/temp.wav"
    # path = "../../segmentcough-master/segmentcough-master/snore.wav"
    data_file = request.files['audio']
    app.logger.info(f'candidate id = {request.form["candidate_id"]}')
    remove_noise = bool(request.form["remove_noise"])
    app.logger.info(f'noise cancellation enabled = {remove_noise}')
    app.logger.info("Obtained file, sending the data for segmentation.")
    # data_file.save(path)
    # output = find_breathing_sound_prop(path)
    output = find_cough_sound_prop(data_file.read(), remove_noise=remove_noise)
    app.logger.info(f"final cough sound result = {output}")
    return output


@app.route("/breath", methods=["GET", "POST"])  # at the end point /
def get_breath_data():
    # path = "../../segmentcough-master/segmentcough-master/breath.wav"
    data_file = request.files['audio']
    app.logger.info(f'candidate id = {request.form["candidate_id"]}')

    output = find_breathing_sound_prop(data_file.read())
    app.logger.info(f"final breath sound result = {output}")

    return output


@app.route("/vowel", methods=["GET", "POST"])  # at the end point /
def get_vowel_data():
    # path = "../../segmentcough-master/segmentcough-master/vowel.wav"
    data_file = request.files['audio']
    app.logger.info(f'candidate id = {request.form["candidate_id"]}')

    output = find_vowel_sound_prop(data_file.read())
    app.logger.info(f"final vowel sound result = {output}")

    return output


@app.route("/blow", methods=["GET", "POST"])  # at the end point /
def get_blow_data():
    # path = "../../segmentcough-master/segmentcough-master/vowel.wav"
    data_file = request.files['audio']
    app.logger.info(f'candidate id = {request.form["candidate_id"]}')

    output = find_blow_sound_prop(data_file.read())
    app.logger.info(f"final blow sound result = {output}")

    return output

@app.route("/speech", methods=["GET", "POST"])  # at the end point /
def get_speech_data():
    # path = "../../segmentcough-master/segmentcough-master/speech.wav"
    data_file = request.files['audio']
    app.logger.info(f'candidate id = {request.form["candidate_id"]}')

    output = find_speech_sound_prop(data_file.read())
    app.logger.info(f"final speech sound result = {output}")

    return output


@app.route("/snore", methods=["GET", "POST"])  # at the end point /
def get_snore_data():
    # path = "../../segmentcough-master/segmentcough-master/snore.wav"
    data_file = request.files['audio']
    app.logger.info(f'candidate id = {request.form["candidate_id"]}')

    output = find_snoring_sound_prop(data_file.read())
    app.logger.info(f"final snore sound result = {output}")

    return output


app.logger.setLevel(logging.DEBUG)
app.logger.propagate = False
app.logger.addHandler(stream_handler)


def handler(event, context):
    if event.get("source") == "serverless-plugin-warmup":
        app.logger.info("WarmUp - Lambda is warm!")
        return {}
    return serverless_wsgi.handle_request(app, event, context)


if __name__ == '__main__':
    # app.logger.addHandler(file_handler)

    app.run(host="127.0.0.1", port=5000, debug=True)
