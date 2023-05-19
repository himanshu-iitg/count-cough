import json

from yamnet.run import get_top_audio_scores

from configuration.constants import COUGH_THRESHOLD, COUGH_INDEX
from segmentcough.ops.segmentation import segment_cough
from utils.input import get_audio


def segregate_cough(binary_file, remove_noise=True):
    """
    --> detects if cough is present in the voice or not
    :param binary_file:
    :param remove_noise:
    :return:
    """
    fs, reduced_noise = get_audio(binary_file, remove_noise)

    # TODO: need to improve segmentation code not workking very well for different cases. Need to study about segmentation theory
    segment, mask = segment_cough(reduced_noise, fs, min_cough_len=0.05, th_l_multiplier=0.05,
                                  th_h_multiplier=3, cough_padding=0.5)
    total_seg = len(segment)
    top, scores = get_top_audio_scores(fs, reduced_noise)
    noise_prob, cough_prob = check_noise_and_cough_prob(top)
    print('prob', cough_prob)

    count = 0
    for i, s in enumerate(segment):
        _top, sc = get_top_audio_scores(fs, s)
        n, cgh = check_noise_and_cough_prob(sc)
        print(f'number = {i}', cgh)
        if cgh > COUGH_THRESHOLD:
            # sf.write(f'no_n_seg_{i}.wav', s, samplerate=fs,
            #     subtype='PCM_16', format='wav')
            count += 1

    data = {'noise_prob': noise_prob, 'cough_prob': str(cough_prob),
            'total_segments': total_seg if total_seg > 0 else 1,
            'cough_segments': count if total_seg > 0 else 1}
    print(data)
    return json.dumps(data)


def check_noise_and_cough_prob(top):
    """
    --> detects if cough is present in the voice or not
    :param input_path:
    :return:
    """
    noise = 1
    prob = 0
    for i, d in enumerate(top):
        if COUGH_INDEX == d[0]:
            noise = i / len(top)
            prob = d[2]
            break
    return noise, prob


if __name__ == '__main__':
    path = '../../segmentcough-master/segmentcough-master/no_n_seg_0.wav'
    segregate_cough(path)
