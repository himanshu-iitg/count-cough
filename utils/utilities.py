from librosa.feature import rms
import soundfile as sf
import numpy as np

from configuration.logger import sound_logger


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
    hop_length = int(min_cough_duration*sr)
    if len(signal.shape) > 1:
        signal = np.mean(signal, axis=1)

    sound_logger.debug(f'Shape of input signal is {signal.shape}')
    sound_logger.info(f'Hop length is {hop_length} for min_cough_duration of {min_cough_duration}')

    energy = rms(y=signal, hop_length=hop_length)[0]
    sound_logger.debug(f'signal energy: max = {np.max(energy)} min = {np.min(energy)}')

    # Normalize the energy values
    normalized_energy = (energy - np.min(energy)) / (np.max(energy) - np.min(energy))

    sound_logger.debug(f'normalized energy: max = {np.max(normalized_energy)}'
                       f' min = {np.min(normalized_energy)}')

    # Set the energy threshold for event detection
    cough_threshold = np.max(normalized_energy) * cough_threshold
    sound_logger.debug(f'cough sound threshold value = {cough_threshold}')

    # stft = np.abs(np.fft.rfft(signal))
    # print(stft.shape)
    min_cough_samples = round(sr * min_cough_duration)
    print('min cough samples', min_cough_samples, min_cough_duration)


    # Find the cough segments
    cough_segments = []
    event_start = None

    for i, value in enumerate(normalized_energy):
        if value >= cough_threshold:
            if event_start is None:
                event_start = i*hop_length
        else:
            if event_start is not None:
                cough_duration = i*hop_length - event_start
                if cough_duration >= min_cough_samples:
                    event_end = i*hop_length + int(padding * sr)
                    event_start -= int(padding * sr)
                    cough_segments.append(signal[event_start: event_end+1])
                event_start = None

    sound_logger.info(f'Total cough segments identified = {len(cough_segments)}')
    sound_logger.debug(f'cough segments identified: {cough_segments}')
    # Convert cough segments to time in seconds
    # cough_segments = [(start / sr, end / sr) for start, end in cough_segments]

    return cough_segments