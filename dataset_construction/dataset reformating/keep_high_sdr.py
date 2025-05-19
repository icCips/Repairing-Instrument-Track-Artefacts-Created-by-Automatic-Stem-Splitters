import os
from pydub import AudioSegment
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt

def safe_read_audio(file_path):
    try:
        data, sr = sf.read(file_path)
        return data, sr
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None, None

def si_sdr(s, s_hat):
    alpha = np.dot(s_hat, s) / np.linalg.norm(s) ** 2   
    sdr = 10 * np.log10(np.linalg.norm(alpha * s) ** 2 / np.linalg.norm(
        alpha * s - s_hat) ** 2)
    return sdr

def si_sdr_from_files(file1, file2):
    """
    Calculate SI-SDR between two audio files.
    
    Args:
        file1 (str): Path to the first audio file (reference signal).
        file2 (str): Path to the second audio file (estimated signal).
    
    Returns:
        float: SI-SDR value in dB.
    """
    # Load audio files
    s, sr1 = safe_read_audio(file1)
    s_hat, sr2 = safe_read_audio(file2)
    
    if s is None or s_hat is None:
        
        return None
    
    # Ensure sampling rates match
    if sr1 != sr2:
        raise ValueError("Sampling rates of the two files must be the same.")
    
    # Truncate or pad to match lengths
    min_len = min(len(s), len(s_hat))
    s = s[:min_len]
    s_hat = s_hat[:min_len]
    
    # Compute SI-SDR
    return si_sdr(s, s_hat)

def keep_hi_sdr_files(base_dir, thresh):
    
    sdrs = []

    #base_dir = "/Volumes/Bank_1/FYP/Model_Architectures/sgmse/datasets/sgsme_vocal_16kHz_5s_chunks"

    # List only directories (not files)
    subfolders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]

    for subfolder in subfolders:
        clean_folder = os.path.join(base_dir, subfolder, "clean")
        noisy_folder = os.path.join(base_dir, subfolder, "noisy")
        
        clean_files = os.listdir(clean_folder)
        noisy_files = os.listdir(noisy_folder)
        
        l = len(clean_files)
        
        for i, clean_file in enumerate(clean_files):
            clean_file_path = os.path.join(clean_folder, clean_file)
            noisy_file_path = os.path.join(noisy_folder, clean_file)
            
            
            # Ensure file exists in noisy folder
            if not os.path.exists(noisy_file_path):
                continue
            
            # Calc si-sdr
            
            sdr = si_sdr_from_files(clean_file_path, noisy_file_path)
            
            if sdr is None:
                
                print(f"removing low SI-SDR files - {i+1}/{l} **")
                
                os.remove(clean_file_path)
                if os.path.exists(noisy_file_path):
                    os.remove(noisy_file_path)
            
            elif sdr > thresh:
                
                print(f"removing low SI-SDR files - {i+1}/{l}")
                
                sdrs.append(sdr)
                
            else:
                
                print(f"removing low SI-SDR files - {i+1}/{l} *")
                
                os.remove(clean_file_path)
                if os.path.exists(noisy_file_path):
                    os.remove(noisy_file_path)

