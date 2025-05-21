import random
import soundfile as sf
import numpy as np

def cut_audio(audio_file, sr, start_sample, end_sample):
    segment_length = 30 * sr  # 30 seconds worth of samples

    if len(audio_file) < segment_length:
        padding_length = segment_length - len(audio_file)
        segment = np.pad(audio_file, ((0, padding_length), (0, 0)), mode='constant')
    else:
        segment = audio_file[:segment_length]

    return segment


def generate_sample_indices(length_in_samples, sample_rate):

    min_excerpt_len_samples = 30 * sample_rate  # 30 seconds in samples
    max_excerpt_len_samples = 50 * sample_rate  # 50 seconds in samples

    start_sample = random.randrange(0, max(1, length_in_samples - min_excerpt_len_samples))
    excerpt_len_samples = random.randrange(min_excerpt_len_samples, max_excerpt_len_samples)
    
    end_sample = min(start_sample + excerpt_len_samples, length_in_samples)
    
    return start_sample, end_sample