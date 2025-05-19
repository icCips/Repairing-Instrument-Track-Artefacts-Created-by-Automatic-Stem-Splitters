import os
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt

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
    s, sr1 = sf.read(file1)
    s_hat, sr2 = sf.read(file2)
    
    # Ensure sampling rates match
    if sr1 != sr2:
        raise ValueError("Sampling rates of the two files must be the same.")
    
    # Truncate or pad to match lengths
    min_len = min(len(s), len(s_hat))
    s = s[:min_len]
    s_hat = s_hat[:min_len]
    
    # Compute SI-SDR
    return si_sdr(s, s_hat)

noisy_sdrs = []
enhanced_sdrs = []
delta = []

base_dir = "/Volumes/Bank_1/FYP/Model_Architectures/sgmse/datasets/sgsme_vocal_16kHz_5s_chunks"
enhanced_dir = "/Volumes/Bank_1/FYP/Model_Architectures/sgmse/datasets/enhanced_5s_hi_sdr"

# List only directories (not files)
subfolders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]

for subfolder in subfolders:
    clean_folder = os.path.join(base_dir, subfolder, "clean")
    noisy_folder = os.path.join(base_dir, subfolder, "noisy")
    
    clean_files = os.listdir(clean_folder)
    l = len(clean_files)
    
    for i, clean_file in enumerate(clean_files):
        clean_file_path = os.path.join(clean_folder, clean_file)
        noisy_file_path = os.path.join(noisy_folder, clean_file)
        enhanced_file_path = os.path.join(enhanced_dir, clean_file)
        
        # Ensure files exist
        if not os.path.exists(noisy_file_path) or not os.path.exists(enhanced_file_path):
            continue
        
        # Compute SI-SDR values
        noisy_sdr = si_sdr_from_files(clean_file_path, noisy_file_path)
        enhanced_sdr = si_sdr_from_files(clean_file_path, enhanced_file_path)
        delta.append(enhanced_sdr - noisy_sdr)
        
        
        print(f"Processing {i+1}/{l} - N: {noisy_sdr:.2f} dB - E: {enhanced_sdr:.2f} dB - Δ: {enhanced_sdr - noisy_sdr:.2f} dB")
        
        noisy_sdrs.append(noisy_sdr)
        enhanced_sdrs.append(enhanced_sdr)

# Compute averages
avg_noisy_sdr = np.mean(noisy_sdrs)
avg_enhanced_sdr = np.mean(enhanced_sdrs)

print(f"Average Noisy SI-SDR: {avg_noisy_sdr:.2f} dB")
print(f"Average Enhanced SI-SDR: {avg_enhanced_sdr:.2f} dB")
print(f"Average Δ: {np.mean(delta):.2f} dB")

# Plot histograms
plt.figure(figsize=(8, 5))
plt.hist(noisy_sdrs, bins=30, edgecolor='black', alpha=0.7, label='Noisy')
plt.hist(enhanced_sdrs, bins=30, edgecolor='black', alpha=0.7, label='Enhanced')
plt.xlabel("SI-SDR (dB)")
plt.ylabel("Frequency")
plt.title("SI-SDR Histogram")
plt.legend()
plt.grid(True)
plt.show()
