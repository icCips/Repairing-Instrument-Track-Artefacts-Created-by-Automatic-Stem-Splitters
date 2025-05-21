import os
import shutil

folder_mapping = {
    "Bass": ["bass"],
    "Drums": [
        "drum", "kick", "snare", "overheads", "tom", "tambourine", "hihat", "clap", "cymbal", "shaker", "percussion", 
        "taiko", "rimshot", "loop", "conga", "bongo", "djembe", "hi-hat", "ride", "crash", "bell", "stave", "floor tom",
        "marching", "timpani", "cajon", "darbuka", "tabla", "bongos", "conga", "batucada", "bata", "frame drum", 
        "woodblock", "cabasa", "guiro", "metal", "drum kit", "electronic drum", "electronic percussion"
    ],
    "Voice": ["vox", "choir", "speech"],
    "Room": ["room"],
    "Other": []
}

def group_files(dataset_folder):
    print("Grouping files...")
    
    base_dir = os.path.join(dataset_folder, "raw_unzipped")

    for batch_folder in os.listdir(base_dir):
        batch_folder_path = os.path.join(base_dir, batch_folder)
        
        if os.path.isdir(batch_folder_path):
            for multitrack_folder in os.listdir(batch_folder_path):
                multitrack_folder_path = os.path.join(batch_folder_path, multitrack_folder)
                
                if os.path.isdir(multitrack_folder_path):

                    for subfolder in folder_mapping.keys():
                        subfolder_path = os.path.join(multitrack_folder_path, subfolder)
                        os.makedirs(subfolder_path, exist_ok=True)
                    
                    for filename in os.listdir(multitrack_folder_path):
                        file_path = os.path.join(multitrack_folder_path, filename)
                        
                        if os.path.isfile(file_path):

                            destination_folder = "Other"
                            for subfolder, keywords in folder_mapping.items():
                                if any(keyword.lower() in filename.lower() for keyword in keywords):
                                    destination_folder = subfolder
                                    break
                            
                            destination_path = os.path.join(multitrack_folder_path, destination_folder, filename)
                            
                            try:
                                shutil.move(file_path, destination_path)
                            except FileNotFoundError:
                                print(f"File not found during move: {file_path}")
                            except shutil.Error as e:
                                print(f"Error moving file {file_path}: {e}")
                    
                    print(f"Processed files in: {multitrack_folder_path}")

    print("All files moved successfully.")
