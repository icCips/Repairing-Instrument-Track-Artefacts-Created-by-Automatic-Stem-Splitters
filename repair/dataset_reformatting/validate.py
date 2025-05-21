import os
from pydub import AudioSegment

def validate(base_dir):
    
    subfolders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]

    for subfolder in subfolders:
        
        clean_folder = os.path.join(base_dir, subfolder, "clean")
        noisy_folder = os.path.join(base_dir, subfolder, "noisy")
        
        clean_files = os.listdir(clean_folder)
        noisy_files = os.listdir(noisy_folder)
        
        l = len(noisy_files)
        
        for i, noisy_file in enumerate(noisy_files):
            
            clean_file_path = os.path.join(clean_folder, noisy_file)
            noisy_file_path = os.path.join(noisy_folder, noisy_file)

            if not os.path.exists(clean_file_path):
                
                print(f"validating - {i+1}/{l} *")
                
                os.remove(noisy_file_path)
                
            else:
                
                print(f"validating - {i+1}/{l}")
        
        l = len(clean_files)
                
        for i, clean_file in enumerate(clean_files):
            
            clean_file_path = os.path.join(clean_folder, clean_file)
            noisy_file_path = os.path.join(noisy_folder, clean_file)
            
            if not os.path.exists(noisy_file_path):
                
                print(f"validating - {i+1}/{l} *")
                
                os.remove(clean_file_path)
                
            else:
                
                print(f"validating - {i+1}/{l}")