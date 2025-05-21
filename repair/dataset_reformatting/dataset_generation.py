import os
import shutil
import random as r

def generate_dataset(input, output, type):
    # the .DS_Store is a MacOS specific system file. if you are not using MacOS, set this variable to ""
    ds = ".DS_Store"

    #input = "/Volumes/Bank_1/FYP/Dataset/generated_mixes"

    #output = "/Volumes/Bank_1/FYP/Dataset/sgmse_vocal"
    
    type_suffix = type[1:]

    os.makedirs(output)

    # split

    train_split = 0.8
    valid_split = 0.1
    test_split = 0.1

    train_path = os.path.join(output, "train")
    os.makedirs(train_path)

    train_clean_path = os.path.join(train_path, "clean")
    os.makedirs(train_clean_path)

    train_noisy_path = os.path.join(train_path, "noisy")
    os.makedirs(train_noisy_path)

    valid_path = os.path.join(output, "valid")
    os.makedirs(valid_path)

    valid_clean_path = os.path.join(valid_path, "clean")
    os.makedirs(valid_clean_path)

    valid_noisy_path = os.path.join(valid_path, "noisy")
    os.makedirs(valid_noisy_path)

    test_path = os.path.join(output, "test")
    os.makedirs(test_path)

    test_clean_path = os.path.join(test_path, "clean")
    os.makedirs(test_clean_path)

    test_noisy_path = os.path.join(test_path, "noisy")
    os.makedirs(test_noisy_path)

    # iterate

    processed = []

    songs = os.listdir(input)

    if ds in songs:
        
        songs.remove(ds)

    songs_amt = len(songs)

    for i, song in enumerate(songs):
        
        print(f"generating dataset: processing song - {i+1}/{songs_amt}")
        
        song_path = os.path.join(input, song)
        
        vers = os.listdir(song_path)
        
        if ds in vers:
            
            vers.remove(ds)
            
        for ver in vers:
            
            ver_path = os.path.join(song_path, ver)
            
            sub_vers = os.listdir(ver_path)
            
            if ds in sub_vers:
                
                sub_vers.remove(ds)
            
            stem_paths = []
            
            for sub_ver in sub_vers:
                
                if not sub_ver.endswith(".wav"):
                    
                    sub_ver_path = os.path.join(ver_path, sub_ver)
                    
                    insts = os.listdir(sub_ver_path)
                    
                    if ds in insts:
                        
                        insts.remove(ds)
                        
                    for inst in insts:
                        
                        if inst.endswith(type_suffix+".wav"):
                            
                            stem_paths.append(os.path.join(sub_ver_path, inst)) 
                
            file_name = song + "_" + type + "_" + ver + ".wav"
                            
            if len(stem_paths) == 2 and file_name not in processed:
                
                processed.append(file_name)
                
                r_num = r.uniform(0, 1)
                
                if r_num <= train_split:
                    
                    for src_path in stem_paths:
                        
                        if "ai_seperated_stems" in src_path:
                            
                            dst_path = os.path.join(train_noisy_path, file_name)
                            
                            #print(f"copying {src_path} to {dst_path}")
                            
                            shutil.copyfile(src_path, dst_path)
                            
                            
                        elif "true_stems" in src_path:
                            
                            dst_path = os.path.join(train_clean_path, file_name)
                            
                            #print(f"copying {src_path} to {dst_path}")
                            
                            shutil.copyfile(src_path, dst_path)
                            
                        else:
                            
                            print("Error: bad category")
                            
                            
                    
                elif r_num <= valid_split + train_split:
                    
                    for src_path in stem_paths:
                        
                        if "ai_seperated_stems" in src_path:
                            
                            dst_path = os.path.join(valid_noisy_path, file_name)
                            
                            #print(f"copying {src_path} to {dst_path}")
                            
                            shutil.copyfile(src_path, dst_path)
                            
                        elif "true_stems" in src_path:
                            
                            dst_path = os.path.join(valid_clean_path, file_name)
                            
                            #print(f"copying {src_path} to {dst_path}")
                            
                            shutil.copyfile(src_path, dst_path)
                            
                        else:
                            
                            print("Error: bad category")
                            
                            
                    
                elif r_num <= test_split + valid_split + train_split:
                    
                    for src_path in stem_paths:
                        
                        if "ai_seperated_stems" in src_path:
                            
                            dst_path = os.path.join(test_noisy_path, file_name)
                            
                            #print(f"copying {src_path} to {dst_path}")
                            
                            shutil.copyfile(src_path, dst_path)
                            
                        elif "true_stems" in src_path:
                            
                            dst_path = os.path.join(test_clean_path, file_name)
                            
                            #print(f"copying {src_path} to {dst_path}")
                            
                            shutil.copyfile(src_path, dst_path)
                            
                        else:
                            
                            print("Error: bad category")
                            
                            