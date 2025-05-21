import os
from pydub import AudioSegment
from pydub.silence import detect_silence

def remove_silent_files(base_dir):
    #base_dir = "/Volumes/Bank_1/FYP/Model_Architectures/sgmse/datasets/sgsme_test_5s"

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
            audio = AudioSegment.from_file(clean_file_path, format="wav")

            silence_threshold = -50  # in dBFS
            chunk_size = 4000  # in ms

            silence_ranges = detect_silence(audio, min_silence_len=chunk_size, silence_thresh=silence_threshold)

            if len(silence_ranges) != 0:
                print(f"removing silent files - {i+1}/{l} - Silence detected in {clean_file}")

                os.remove(clean_file_path)
                
                if os.path.exists(noisy_file_path):
                    os.remove(noisy_file_path)
                
            else:
                
                print(f"removing silent files - {i+1}/{l}")