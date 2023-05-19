from flask import Flask, request
from flask_cors import CORS

from core.cough import segregate_cough

TOP_N = 5

app = Flask(__name__)  # create an app instance
CORS(app)


@app.route("/cough", methods=["POST"])  # at the end point /
def get_cough_data():
    # path = "temp.wav"
    data_file = request.files['audio']

    # data_file.save(path)
    # data_file.seek(0)

    return segregate_cough(data_file.read())

@app.route("/breath", methods=["POST"])  # at the end point /
def get_cough_data():
    # path = "temp.wav"
    data_file = request.files['audio']

    # data_file.save(path)
    # data_file.seek(0)

    return segregate_cough(data_file.read())

if __name__ == '__main__':
    app.run(debug=True)
