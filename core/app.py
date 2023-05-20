from flask import Flask, request
from flask_cors import CORS
from core.sounds import find_cough_sound_prop, find_breathing_sound_prop, find_vowel_sound_prop, find_speech_sound_prop, \
    find_snoring_sound_prop

app = Flask(__name__)  # create an app instance
CORS(app)


@app.route("/cough", methods=["POST"])  # at the end point /
def get_cough_data():
    # path = "../../segmentcough-master/segmentcough-master/cough.wav"
    data_file = request.files['audio']
    # data_file.save(path)
    # data_file.seek(0)

    return find_cough_sound_prop(data_file.read())

@app.route("/breath", methods=["POST"])  # at the end point /
def get_breath_data():
    # path = "../../segmentcough-master/segmentcough-master/breath.wav"
    data_file = request.files['audio']
    # data_file.save(path)
    # data_file.seek(0)

    return find_breathing_sound_prop(data_file.read())

@app.route("/vowel", methods=["POST"])  # at the end point /
def get_vowel_data():
    # path = "../../segmentcough-master/segmentcough-master/vowel.wav"
    data_file = request.files['audio']
    # data_file.save(path)
    # data_file.seek(0)

    return find_vowel_sound_prop(data_file.read())


@app.route("/speech", methods=["POST"])  # at the end point /
def get_speech_data():
    # path = "../../segmentcough-master/segmentcough-master/speech.wav"
    data_file = request.files['audio']
    # data_file.save(path)
    # data_file.seek(0)

    return find_speech_sound_prop(data_file.read())


@app.route("/snore", methods=["POST"])  # at the end point /
def get_snore_data():
    # path = "../../segmentcough-master/segmentcough-master/snore.wav"
    data_file = request.files['audio']
    # data_file.save(path)
    # data_file.seek(0)

    return find_snoring_sound_prop(data_file.read())

if __name__ == '__main__':
    app.run(debug=True)
