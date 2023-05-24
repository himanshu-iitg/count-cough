from librosa.feature import rms
import soundfile as sf
import numpy as np


def check_noise_and_index_prob(top, index):
    """
    --> detects if cough is present in the voice or not
    :param input_path:
    :return:
    """
    noise = 1
    prob = 0
    for i, d in enumerate(top):
        if index == d[0]:
            noise = i / len(top)
            prob = d[2]
            break
    return noise, prob


def segment_cough_sound(signal, sr, cough_threshold=0.1, min_cough_duration=0.1, padding=0.1):
    # Load the audio file
    # audio_file = "../../segmentcough-master/segmentcough-master/cough.wav"
    # signal, sr = sf.read(audio_file)
    if len(signal.shape) > 1:
        signal = np.mean(signal, axis=1)

    print(signal.shape)

    # Compute short-time Fourier transform (STFT)
    # energy = np.sqrt(np.mean(np.square(signal)))
    # energy = librosa.feature.rms(signal, frame_length=2048, hop_length=512)[0]
    energy = rms(y=signal, hop_length=512)[0]
    print('energy shape', energy.shape)

    # Normalize the energy values
    normalized_centroid = (energy - np.min(energy)) / (np.max(energy) - np.min(energy))

    # Set the energy threshold for event detection
    cough_threshold = np.max(normalized_centroid) * cough_threshold
    # stft = np.abs(np.fft.rfft(signal))
    # print(stft.shape)
    min_cough_samples = round(sr * min_cough_duration)
    print('min cough samples', min_cough_samples, min_cough_duration)


    # Find the cough segments
    cough_segments = []
    event_start = None

    for i, value in enumerate(normalized_centroid):
        if value >= cough_threshold:
            if event_start is None:
                event_start = i*512
        else:
            if event_start is not None:
                cough_duration = i*512 - event_start
                if cough_duration >= min_cough_samples:
                    event_end = i*512 + int(padding * sr)
                    event_start -= int(padding * sr)
                    cough_segments.append(signal[event_start: event_end+1])
                event_start = None

    # for i,s in enumerate(cough_segments):
    #     sf.write(f'temp_{i}.wav', s, sr)
    # Convert cough segments to time in seconds
    # cough_segments = [(start / sr, end / sr) for start, end in cough_segments]

    return cough_segments