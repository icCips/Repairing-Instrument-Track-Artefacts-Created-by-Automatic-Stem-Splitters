import os
import wave
import contextlib
import numpy as np
from scipy.io.wavfile import write


def split_stereo_to_mono(file_path, output_path_left, output_path_right):
    """Splits a stereo WAV file into two mono WAV files."""
    with wave.open(file_path, 'r') as stereo_wav:
        params = stereo_wav.getparams()
        n_channels, sample_width, frame_rate, n_frames, comp_type, comp_name = params

        if n_channels != 2:  # Check if the file is stereo
            print(f"Skipping {file_path}, not a stereo file.")
            return False

        # Read stereo frames and convert to mono
        frames = stereo_wav.readframes(n_frames)
        stereo_data = np.frombuffer(frames, dtype=np.int16).reshape(-1, 2)
        left_channel = stereo_data[:, 0]
        right_channel = stereo_data[:, 1]

        # Save left channel
        write(output_path_left, frame_rate, left_channel)

        # Save right channel
        write(output_path_right, frame_rate, right_channel)

        return True


def check_dataset(folder_path):
    subfolders = ['clean', 'noisy']
    files_to_split = []

    for subset in ['train', 'test', 'valid']:
        paths = {sf: os.path.join(folder_path, subset, sf) for sf in subfolders}

        for sf in subfolders:
            other_sf = 'clean' if sf == 'noisy' else 'noisy'
            files = os.listdir(paths[sf])
            l = len(files)

            for i, file in enumerate(files):
                print(f"Checking {i+1}/{l} in {subset}/{sf}")

                sf_file_path = os.path.join(paths[sf], file)
                other_sf_file_path = os.path.join(paths[other_sf], file)

                # Check if sibling file exists
                '''
                if not os.path.exists(other_sf_file_path):
                    print(f"Marking {sf_file_path} for deletion (no sibling found)")
                    os.remove(sf_file_path)
                    continue
                '''
                '''
                if sf == 'clean':
                    # Check if both files are the same length
                    with contextlib.closing(wave.open(sf_file_path, 'r')) as sf_wav:
                        with contextlib.closing(wave.open(other_sf_file_path, 'r')) as other_sf_wav:
                            sf_length = sf_wav.getnframes()
                            other_sf_length = other_sf_wav.getnframes()

                            if sf_length != other_sf_length:
                                print(f"Marking {sf_file_path} and {other_sf_file_path} for deletion (mismatched lengths)")
                                os.remove(sf_file_path)
                                os.remove(other_sf_file_path)
                                continue
                '''
                if sf == 'noisy':
                    # Check if the file is stereo
                    with wave.open(sf_file_path, 'r') as wav_file:
                        if wav_file.getnchannels() == 2:
                            base_name, ext = os.path.splitext(file)
                            output_path_left = os.path.join(paths[sf], f"{base_name}_L{ext}")
                            output_path_right = os.path.join(paths[sf], f"{base_name}_R{ext}")
                            files_to_split.append((sf_file_path, output_path_left, output_path_right))

    return files_to_split


def split_all(files_to_split):
    for i, (file_path, output_path_left, output_path_right) in enumerate(files_to_split):
        print(f"Splitting {i+1}/{len(files_to_split)}: {file_path}")
        if split_stereo_to_mono(file_path, output_path_left, output_path_right):
            print(f"Split {file_path} into {output_path_left} and {output_path_right}")
            os.remove(file_path)
        else:
            print(f"Failed to split {file_path}")


# Provide the root directory containing 'sgmse_vocal_16kHz'
dataset_root = "datasets/sgmse_vocal_16kHz"

# Step 1: Check the dataset
files_to_split = check_dataset(dataset_root)

# Step 2: Split all stereo files into mono
split_all(files_to_split)
