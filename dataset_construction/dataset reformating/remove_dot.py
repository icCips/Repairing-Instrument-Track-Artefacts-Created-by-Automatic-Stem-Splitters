import os
import time
base_dir = "/Volumes/Bank_1/FYP/Dataset/sgmse_drums_16kHz_5s_chunks"

# List only directories (not files)
subfolders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]

for subfolder in subfolders:
    
    clean_folder = os.path.join(base_dir, subfolder, "clean")
    noisy_folder = os.path.join(base_dir, subfolder, "noisy")
    
    clean_files = os.listdir(clean_folder)
    noisy_files = os.listdir(noisy_folder)
    
    l = len(clean_files)
    
    for i, clean_file in enumerate(clean_files):
        
        print(f"{i+1}/{l}")
        
        clean_file_path = os.path.join(clean_folder, clean_file)
        
        if clean_file.startswith("._"):
            
            time.sleep(1)
            
            os.remove(clean_file_path)
    
    l = len(noisy_files)
    
    for i, noisy_file in enumerate(noisy_files):
        
        print(f"{i+1}/{l}")
        
        noisy_file_path = os.path.join(noisy_folder, noisy_file)
        
        if noisy_file_path.startswith("._"):
            
            time.sleep(1)
            
            os.remove(noisy_file_path)