import os
from pydub import AudioSegment

def remove_short_files(base_dir):
    #base_dir = "/Volumes/Bank_1/FYP/Model_Architectures/sgmse/datasets/sgsme_test_5s_chunks"

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

            # Check if duration is less than 5 seconds
            if len(audio) < 5000:  # Duration in milliseconds
                print(f"removing short files: {i+1}/{l} - {clean_file} is shorter than 5s")
                
                os.remove(clean_file_path)
                
                if os.path.exists(noisy_file_path):
                    os.remove(noisy_file_path)
                
            else:
                print(f"removing short files: {i+1}/{l}")
