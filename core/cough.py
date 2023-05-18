import json
from pprint import pprint

import noisereduce as nr

from sound_predictor.run import get_audio_scores
import tensorflow as tf

import numpy as np
import io
import soundfile as sf
from segmentcough.ops.segmentation import segment_cough

def segregate_cough(path):
    """
    --> detects if cough is present in the voice or not
    :param input_path:
    :return:
    """
    x, fs = sf.read(io.BytesIO(path), dtype=np.int16)
    # x, fs = sf.read(file=path, dtype=np.int16)
    if len(x.shape) > 1:
        x = np.mean(x, axis=1)

    wav_data = nr.reduce_noise(y=x, sr=fs, stationary=True)
    reduced_noise = wav_data / tf.int16.max

    # TODO: need to improve segmentation code not workking very well for different cases. Need to study about segmentation theory
    segment, mask = segment_cough(reduced_noise, fs, min_cough_len=0.05, th_l_multiplier=0.05, th_h_multiplier=3, cough_padding=0.5)

    scores = get_audio_scores(fs, reduced_noise)


    # reduced_noise = nr.reduce_noise(y=x, sr=fs, stationary=True)

    mean_prob2 = cough_probability(scores)
    print('prob', mean_prob2)

    print('len of segment', len(segment))

    count = 0
    for i, s in enumerate(segment):
        s = nr.reduce_noise(s, fs, stationary=True)
        sc, embeddings, spectrogram = yamnet(s)
        print(f'number = {i}', cough_probability(sc))
        if cough_probability(sc)>0.3:
            # sf.write(
            #     f'no_n_seg_{i}.wav',
            #     s,
            #     samplerate=fs,
            #     subtype='PCM_16',
            #     format='wav'
            # )
            count+=1

    mean_scores = np.mean(scores, axis=0)
    top_class_indices = np.argsort(mean_scores)[::-1][:TOP_N]
    yticks = range(0, TOP_N, 1)
    pprint([(top_class_indices[x], class_names[top_class_indices[x]], mean_scores[top_class_indices[x]]) for x in yticks])

    # plt.imshow(scores[:, top_class_indices].T, aspect='auto', interpolation='nearest', cmap='gray_r')
    # Compensate for the patch_window_seconds (0.96s) context window to align with spectrogram.
    # patch_padding = (params.patch_window_seconds / 2) / params.patch_hop_seconds
    # plt.xlim([-patch_padding, scores.shape[0] + patch_padding])
    # Label the top_N classes.
    # plt.yticks(yticks, [class_names[top_class_indices[x]] for x in yticks])
    # _ = plt.ylim(-0.5 + np.array([TOP_N, 0]))
    # plt.savefig('variety.png')
    # return {'segments': [s.tolist() for s in cough_segments], 'mask': mask.tolist()}
    # return json.dumps({'prob2': str(mean_prob2), 'segments': len(cough_segments)})
    print(json.dumps({'prob2': str(mean_prob2), 'segments': count}))
    return json.dumps({'prob2': str(mean_prob2), 'segments': count})
    # return json.dumps({'prob': str(prob), 'prob2': str(prob2), 'segments': len(cough_segments)})


def cough_probability(scores):
    """
    --> detects if cough is present in the voice or not
    :param input_path:
    :return:
    """
    prob = np.mean(scores[:, 42])
    # prob = np.mean(scores[:, 36])
    return prob