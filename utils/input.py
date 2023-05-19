import io

import noisereduce as nr
import numpy as np
import soundfile as sf
import tensorflow as tf


def get_audio(binary_file, remove_noise):
    """
    --> Read audio from binary data and remove stationary noise if required
    :param binary_file:
    :param remove_noise:
    :return:
    """
    wav_data, fs = sf.read(io.BytesIO(binary_file), dtype=np.int16)
    # wav_data, fs = sf.read(file=binary_file, dtype=np.int16)
    if len(wav_data.shape) > 1:
        wav_data = np.mean(wav_data, axis=1)
    if remove_noise:
        wav_data = nr.reduce_noise(y=wav_data, sr=fs, stationary=True)
        reduced_noise = wav_data / tf.int16.max
    else:
        reduced_noise = wav_data / tf.int16.max
    return fs, reduced_noise
