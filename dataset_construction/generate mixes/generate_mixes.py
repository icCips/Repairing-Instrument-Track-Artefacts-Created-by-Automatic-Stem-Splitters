import process_track as pt
import time_code_util as tcu
import os
import soundfile as sf
import numpy as np
from scipy.signal import resample

SR = 44100

base_dir = "songs"
base_dest = "generated_mixes"

def resample_audio(data, samplerate, target_samplerate=SR):
    
    if samplerate != target_samplerate:
        # Calculate the number of samples needed for the new sample rate
        num_samples = int(len(data) * target_samplerate / samplerate)
        
        # Resample the data
        resampled_data = resample(data, num_samples)
        
        print(f"Sample rate was {samplerate}. Changed to {target_samplerate}.")
        return resampled_data
    else:
        return data

def DFS(directory):
    for entry in os.listdir(directory):
        entry_path = os.path.join(directory, entry)
        
        if os.path.isdir(entry_path):
            result = DFS(entry_path)
            if result:  
                return result
        
        elif os.path.isfile(entry_path) and entry.lower().endswith('.wav'):
            # Skip macOS-specific dot-underscore files
            if entry.startswith("._"):
                continue
            
            try:
                print(entry_path)
                audio, sr = sf.read(entry_path)
                return tcu.generate_sample_indices(len(audio), sr)
            except Exception as e:
                print(f"Error reading {entry_path}: {e}")
    
    return None

'''
def sum_audio_files(stems, level):
    
    if not stems:
        return None, None
    
    sample_rate = None
    summed_audio = None
    
    for audio in stems:
        
        normalized_audio = pt.normalize_audio(audio[0], audio[1], -5)
        
        if sample_rate is None:
            sample_rate = audio[1]
            summed_audio = np.zeros_like(normalized_audio)
        elif audio[1] != sample_rate:
            raise ValueError("Sample rates do not match")
        
        summed_audio += normalized_audio
    
    normalised_audio = pt.normalize_audio(summed_audio, sample_rate, level)
    
    return normalised_audio, sample_rate
'''

def sum_audio_files(stems, level):
    if not stems:
        return None
    
    sample_rate = None
    summed_audio = None
    
    for audio in stems:
        # Normalize individual stem
        normalized_audio = pt.normalize_audio(audio[0], audio[1], -5)
        
        if sample_rate is None:
            sample_rate = audio[1]
            summed_audio = np.zeros_like(normalized_audio)
        elif audio[1] != sample_rate:
            print(stems)
            raise ValueError("Sample rates do not match")
        
        summed_audio += normalized_audio
    
    # Check for clipping and limit the audio
    max_amplitude = np.max(np.abs(summed_audio))
    if max_amplitude > 1.0:
        summed_audio /= max_amplitude  # Normalize the sum to prevent clipping
    
    # Normalize the final summed audio
    normalised_audio = pt.normalize_audio(summed_audio, SR, level)
    
    return normalised_audio

def generate_mixes(version):
    
    for batch_folder in os.listdir(base_dir):
        batch_folder_path = os.path.join(base_dir, batch_folder)
        
        # iterate through multitrack batches
        
        if os.path.isdir(batch_folder_path):
            
            print(f"processing {batch_folder}")
            print()
            
            for multitrack_folder in os.listdir(batch_folder_path):
                multitrack_folder_path = os.path.join(batch_folder_path, multitrack_folder)
                
                dest_path = os.path.join(base_dest, multitrack_folder)
                vers = os.listdir(dest_path) if os.path.exists(dest_path) else []
                
                if version in vers:
                    
                    print(f"{version} has already been generated, skipping")
                    
                    continue
                
                
                # iterate through multitracks
                
                if os.path.isdir(multitrack_folder_path):
                    
                    print(f"processing {multitrack_folder}")
                    print()
                    
                    se_tup = DFS(multitrack_folder_path)
                    
                    if se_tup is None:
                        
                        continue
                    
                    start = se_tup[0]
                    
                    end = se_tup[1]
                    
                    grouped_stems = []
                    
                    for inst_grp in os.listdir(multitrack_folder_path):
                        
                        # iterate through instrument group folders
                        
                        if inst_grp.lower() == 'room':
                            
                            continue
                        
                        inst_grp_path = os.path.join(multitrack_folder_path, inst_grp)
                        
                        if os.path.isdir(inst_grp_path):
                            
                            stems = []
                            
                            for file_name in os.listdir(inst_grp_path):
                                
                                # iterate through tracks
                                
                                if file_name.startswith('._'):
                                    # ignore system files
                                    continue
                                    
                                if pt.dropout():
                                    # random dropouts
                                    continue
                                
                                file_path = os.path.join(inst_grp_path, file_name)
                                
                                if os.path.isfile(file_path) and file_name.lower().endswith('.wav'):
                                    
                                    # read audio
                                    audio, sr = sf.read(file_path)
                                    
                                    audio = audio.astype(np.float32)
                                    
                                    audio = resample_audio(audio, sr)
                                    
                                    # convert to stereo
                                    if audio.ndim == 1:
                                        
                                        audio = np.tile(audio[:, np.newaxis], (1, 2))
                                    
                                    # process audio
                                    processed_audio, sr = pt.process(file_name, audio, sr, start, end, inst_grp)
                                    
                                    if sr == -2:
                                        # silence
                                        continue
                                    
                                    #append to stems list
                                    stems.append((processed_audio, SR))
                                
                            grouped_stems_folder = os.path.join(base_dest, multitrack_folder, version, 'true_stems')
                            os.makedirs(grouped_stems_folder, exist_ok=True)
                            
                            # sum stems to group stem (-10dbLUFS)
                            summed_audio = sum_audio_files(stems, -10)
                            
                            # save it
                            if summed_audio is not None:
                                grouped_stems.append((summed_audio, SR))
                                summed_destination_path = os.path.join(grouped_stems_folder, inst_grp + '.wav')
                                sf.write(summed_destination_path, summed_audio, SR)
                    
                    # sum group stems to create mixdown
                    mixdown = sum_audio_files(grouped_stems, 0)
                    
                    master, _ = pt.process("_master", mixdown, SR)
                    
                    norm_master = pt.normalize_audio(master, SR, -0.5)
                    
                    if norm_master is not None:
                        
                        master_destination_path = os.path.join(base_dest, multitrack_folder, version, multitrack_folder + '_master.wav')
                        sf.write(master_destination_path, norm_master, SR)
                        
                    if pt.is_white_noise(master_destination_path):
                
                        print("WARNING: White Noise Detected")
                        print()

generate_mixes("ver_1")
generate_mixes("ver_2")
generate_mixes("ver_3")
#generate_mixes("ver_4")
#generate_mixes("ver_5")
#generate_mixes("ver_6")
#generate_mixes("ver_7")
#generate_mixes("ver_8")
#generate_mixes("ver_9")
#generate_mixes("ver_10")