import call as c
import os
import glob

base_dir = "/Volumes/Bank_1/FYP/Dataset/generated_mixes"

num_versions = 5880

def seperate_dataset():
    
    i=0

    for multitrack_folder in os.listdir(base_dir):
        multitrack_folder_path = os.path.join(base_dir, multitrack_folder)
        
        for ver_folder in os.listdir(multitrack_folder_path):
            ver_folder_path = os.path.join(multitrack_folder_path, ver_folder)
            
            i=i+1
            
            print(f"\nprocessing {ver_folder_path} \n{i}/5880\n")
            
            wav_files = glob.glob(os.path.join(ver_folder_path, "*.wav"))
            
            if wav_files:
                
                if len(wav_files) > 1:
                    
                    print("ver_folder_path")
                    raise FileNotFoundError("multiple wav files in one ver folder")
                
                mixdown = wav_files[0]
                
                mixdown_path = os.path.join(ver_folder_path, mixdown)
                print(mixdown_path)
                
            else:
                
                raise FileNotFoundError("missing wav_file")
            
            ai_stem_folder = "ai_seperated_stems"
            ai_stem_folder_path = os.path.join(ver_folder_path, ai_stem_folder)
            
            if not os.path.exists(ai_stem_folder_path):
                
                os.makedirs(ai_stem_folder_path)
                print()
                
            else:
                
                print(f"\nai seperation already exists, skipping")
                
                continue
            
            # seperation
            
            c.predict(mixdown_path, ai_stem_folder_path)
        
seperate_dataset()
        
        
        