import json

from yamnet.config.constants import HOP_SECONDS
from yamnet.run import get_top_audio_scores
import soundfile as sf
from configuration.logger import sound_logger
from configuration.constants import COUGH_THRESHOLD, COUGH_INDEX, BREATH_INDEX, BREATH_THRESHOLD, VOWEL_INDEX, \
    VOWEL_THRESHOLD, SPEECH_THRESHOLD, SNORE_INDEX, SNORE_THRESHOLD, SPEECH_INDEX
# from segmentcough.ops.segmentation import segment_cough
from utils.input import get_audio
from utils.utilities import check_noise_and_index_prob, segment_cough_sound


def get_sound_prop_for_index(binary_file, remove_noise, index, is_file=False):
    """
    --> Returns the properties of sound like the top_n sounds present noise and index probability
        and actual processed sound data
    :param binary_file:
    :param remove_noise:
    :param index:
    :return:
    """
    fs, reduced_noise = get_audio(binary_file, remove_noise, is_file)
    top, scores = get_top_audio_scores(fs, reduced_noise)
    sound_logger.info(f'most significant sounds are: {top}')
    noise_prob, index_prob = check_noise_and_index_prob(top, index)
    return fs, reduced_noise, noise_prob, index_prob


def find_cough_sound_prop(binary_file, remove_noise=True, is_file=False):
    """
    --> detects if cough is present in the voice or not
    :param binary_file:
    :param remove_noise:
    :return:
    """
    fs, reduced_noise, noise_prob, cough_prob = \
        get_sound_prop_for_index(binary_file, remove_noise, COUGH_INDEX, is_file)

    # segment, mask = segment_cough(reduced_noise, fs, min_cough_len=0.05, th_l_multiplier=0.05,
    #                               th_h_multiplier=3, cough_padding=0.5)
    segment = segment_cough_sound(reduced_noise, fs, min_cough_duration=0.05)
    # minimum cough duration of 0.5 secs can be used for finding breathing, speech sounds
    # segment = segment_cough_sound(reduced_noise, fs, min_cough_duration=0.5)

    total_seg = len(segment)
    sound_logger.info(f'Total cough segments identified = {total_seg}')

    count = 0
    for i, s in enumerate(segment):
        _top, sc = get_top_audio_scores(fs, s)
        n, cgh = check_noise_and_index_prob(_top, COUGH_INDEX)
        sound_logger.info(f'audio segment number = {i}, cough sound probability = {cgh} '
                          f'with other most significant sounds {_top[:5]}')
        if cgh > COUGH_THRESHOLD:
            # sf.write(f'no_noise_seg_{i}.wav', s, samplerate=fs,
            #     subtype='PCM_16', format='wav')
            count += 1

    data = {'noise_prob': noise_prob, 'cough_prob': float(round(cough_prob, 2)),
            'has_sound': bool(cough_prob >= COUGH_THRESHOLD),
            'total_segments': 1 if total_seg == 0 and cough_prob >= COUGH_THRESHOLD else total_seg,
            'cough_segments': 1 if total_seg == 0 and cough_prob >= COUGH_THRESHOLD else count}
    return json.dumps(data)


def find_breathing_sound_prop(binary_file, remove_noise=False):
    """
    --> detects if cough is present in the voice or not
    :param binary_file:
    :param remove_noise:
    :return:
    """
    fs, reduced_noise, noise_prob, breath_prob = \
        get_sound_prop_for_index(binary_file, remove_noise, BREATH_INDEX)

    data = {'noise_prob': noise_prob, 'breath_prob': float(round(breath_prob, 2)),
            'has_sound': bool(breath_prob >= BREATH_THRESHOLD)}
    print(data)
    return json.dumps(data)


def find_vowel_sound_prop(binary_file, remove_noise=False):
    """
    --> detects if cough is present in the voice or not
    :param binary_file:
    :param remove_noise:
    :return:
    """
    fs, reduced_noise, noise_prob, vowel_prob = \
        get_sound_prop_for_index(binary_file, remove_noise, VOWEL_INDEX)

    data = {'noise_prob': noise_prob, 'vowel_prob': float(round(vowel_prob, 2)),
            'has_sound': bool(vowel_prob >= VOWEL_THRESHOLD)}
    print(data)
    return json.dumps(data)


def find_speech_sound_prop(binary_file, remove_noise=False):
    """
    --> detects if cough is present in the voice or not
    :param binary_file:
    :param remove_noise:
    :return:
    """
    fs, reduced_noise, noise_prob, speech_prob = \
        get_sound_prop_for_index(binary_file, remove_noise, SPEECH_INDEX)

    data = {'noise_prob': noise_prob, 'speech_prob': float(round(speech_prob, 2)),
            'has_sound': bool(speech_prob >= SPEECH_THRESHOLD)}
    print(data)
    return json.dumps(data)


def find_snoring_sound_prop(binary_file, remove_noise=False):
    """
    --> detects if cough is present in the voice or not
    :param binary_file:
    :param remove_noise:
    :return:
    """
    fs, reduced_noise = get_audio(binary_file, remove_noise)

    top, scores = get_top_audio_scores(fs, reduced_noise)
    # print(top)
    noise_prob, snore_prob = check_noise_and_index_prob(top, SNORE_INDEX)
    duration = HOP_SECONDS*sum([1 for n in scores[:, SNORE_INDEX] if n >= SNORE_THRESHOLD])

    data = {'noise_prob': noise_prob, 'snore_prob': float(round(snore_prob, 2)),
            'has_sound': bool(snore_prob >= SNORE_THRESHOLD),
            'snoring_duration': duration}
    print(data)
    return json.dumps(data)


if __name__ == '__main__':
    path = '../../segmentcough-master/segmentcough-master/no_n_seg_0.wav'
    find_cough_sound_prop(path)
