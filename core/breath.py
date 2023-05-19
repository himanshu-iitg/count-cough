import json

from yamnet.run import get_top_audio_scores
from configuration.constants import BREATH_INDEX, BREATH_THRESHOLD
from utils.input import get_audio


def find_breathing_prob(binary_file, remove_noise=False):
    """
    --> detects if cough is present in the voice or not
    :param binary_file:
    :param remove_noise:
    :return:
    """
    fs, reduced_noise = get_audio(binary_file, remove_noise)

    top, scores = get_top_audio_scores(fs, reduced_noise)
    noise_prob, breath_prob = check_noise_and_breath_prob(top)

    data = {'noise_prob': noise_prob, 'breath_prob': str(breath_prob),
            'has_breathing_sound': breath_prob > BREATH_THRESHOLD}
    print(data)
    return json.dumps(data)


def check_noise_and_breath_prob(top):
    """
    --> detects if cough is present in the voice or not
    :param input_path:
    :return:
    """
    noise = 1
    prob = 0
    for i, d in enumerate(top):
        if BREATH_INDEX == d[0]:
            noise = i / len(top)
            prob = d[2]
            break
    return noise, prob


if __name__ == '__main__':
    path = '../../segmentcough-master/segmentcough-master/no_n_seg_0.wav'
    find_breathing_prob(path)
