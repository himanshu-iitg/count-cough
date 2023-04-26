import json
import os

import librosa
import uvicorn
import pickle
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from scipy.io import wavfile

from configuration.constants import COUGH_MODEL_SCALAR, COUGH_MODEL
from segmentcough.ops.detection import classify_cough
from segmentcough.ops.segmentation import segment_cough

app = FastAPI()

origins = [
  "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class Sound(BaseModel):
    sound_path: str

class Cough(BaseModel):
    input_path: str

with open(COUGH_MODEL, 'rb') as f:
    model = pickle.load(f)

with open(COUGH_MODEL_SCALAR, 'rb') as f:
    scaler = pickle.load(f)


@app.get('/')

def index():
    return {'message': 'This is the homepage of the API '}


def wavfile_to_librosa(s_wave):
    nbits = 16
    s_wave /= 2 ** (nbits - 1)
    return s_wave

@app.post('/cough')
def is_cough_detected(data: Cough):
    """
    --> detects if cough is present in the voice or not
    :param input_path:
    :return:
    """
    recieved = data.dict()
    input_path = recieved['input_path']
    fs, x = wavfile.read(input_path)
    prob = classify_cough(x, fs, model, scaler)
    return f'The probability of cough being present in the audio is {prob}'


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


@app.post('/prediction')
def predict(data:Sound):
    recieved = data.dict()
    input_path = recieved['sound_path']
    fs, x = wavfile.read(input_path)
    if is_cough(fs, x):
        l_x = wavfile_to_librosa(x)
        l_x, fs = librosa.load(input_path)
        return segregate_cough(l_x, fs)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=4000)