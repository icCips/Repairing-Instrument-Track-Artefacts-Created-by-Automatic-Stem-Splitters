import os
import random

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
        
        r = random.randint(1, 4)

        if r == 4:
            print(f"{i+1}/{l} - RM")

            os.remove(clean_file_path)
            os.remove(noisy_file_path)
            
        else:
            
            print(f"{i+1}/{l}")