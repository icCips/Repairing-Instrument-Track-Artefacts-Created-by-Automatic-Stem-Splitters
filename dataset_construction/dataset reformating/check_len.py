import os
from pydub import AudioSegment
from pydub.silence import detect_silence

base_dir = "/Volumes/Bank_1/FYP/Model_Architectures/sgmse/datasets/sgsme_vocal_16kHz_5s_chunks"

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
        cl_audio = AudioSegment.from_file(clean_file_path, format="wav")
        no_audio = AudioSegment.from_file(noisy_file_path, format="wav")
        
        if len(cl_audio) != len(no_audio):
            print(f"{i+1}/{l} - {clean_file} is not the same length as its noisy counterpart")
            
            exit()
            
            #os.remove(clean_file_path)
            #os.remove(noisy_file_path)
        
        else:
            print(f"Length of clean audio: {len(cl_audio)}")
            print(f"Length of noisy audio: {len(no_audio)}")
            print(f"{i+1}/{l}")

        