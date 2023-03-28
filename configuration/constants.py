import os

BASE_PATH = os.path.abspath(__file__)
COUGH_MODEL = os.path.join(BASE_PATH, '../../segmentcough/models/cough_classifier')
COUGH_MODEL_SCALAR = os.path.join(BASE_PATH, '../../segmentcough/models/cough_classification_scaler')
