import os
import shutil

def find_and_move_wav_files(folder_path, mix_folder_path):
    """Recursively search for .wav or .flac files, move them to the mix folder level, and return True if any are found."""
    files_found = False

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # Ignore files starting with ._
        if filename.startswith("._"):
            continue
        
        if os.path.isfile(file_path) and (filename.lower().endswith('.wav') or filename.lower().endswith('.flac')):
            # Destination path in the mix folder
            dest_path = os.path.join(mix_folder_path, os.path.basename(file_path))
            
            try:
                # Move the file to the mix folder level
                shutil.move(file_path, dest_path)
                files_found = True
            except shutil.SameFileError:
                print(f"File already exists: {dest_path}")
            except FileNotFoundError:
                print(f"File not found: {file_path}")
        
        elif os.path.isdir(file_path):
            # Recursively search in the subfolder
            if find_and_move_wav_files(file_path, mix_folder_path):
                files_found = True
    
    return files_found  # Return whether any .wav or .flac files were found

def delete_non_wav_flac_files(folder_path):
    """Delete all non .wav and non .flac files in the specified folder."""
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # Delete the file if it is not a .wav or .flac
        if os.path.isfile(file_path) and not (filename.lower().endswith('.wav') or filename.lower().endswith('.flac')):
            os.remove(file_path)
            print(f"Deleted non-wav/flac file: {file_path}")

def delete_subfolders(folder_path):
    """Delete all subfolders in the specified folder."""
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            try:
                shutil.rmtree(dir_path)
                print(f"Deleted subfolder: {dir_path}")
            except OSError as e:
                print(f"Error deleting folder {dir_path}: {e}")

# Define the path to the raw_unzipped folder
base_dir = "/Volumes/Bank 1/FYP/Dataset/raw_unzipped"

# Initialize a counter for mix folders without .wav or .flac files
folders_deleted = 0

# Iterate through each batch folder in the raw_unzipped folder
for batch_folder in os.listdir(base_dir):
    batch_folder_path = os.path.join(base_dir, batch_folder)
    
    if os.path.isdir(batch_folder_path):
        # Iterate through each subfolder inside the batch folder
        for mix_folder in os.listdir(batch_folder_path):
            mix_folder_path = os.path.join(batch_folder_path, mix_folder)
            
            if os.path.isdir(mix_folder_path):
                # Check for .wav or .flac files and move them up to the mix folder level
                has_wav_or_flac = find_and_move_wav_files(mix_folder_path, mix_folder_path)
                
                if not has_wav_or_flac:
                    # No .wav or .flac files found, delete the entire mix folder
                    shutil.rmtree(mix_folder_path)
                    folders_deleted += 1
                    print(f"Deleted folder without .wav or .flac file: {mix_folder_path}")
                else:
                    # Delete non .wav/.flac files in the mix folder
                    delete_non_wav_flac_files(mix_folder_path)
                    
                    # Delete any remaining subfolders in the mix folder
                    delete_subfolders(mix_folder_path)
                    
                    print(f"Moved files, deleted non-wav/flac files, and cleaned up folder: {mix_folder_path}")

# Print the total number of folders deleted
print(f"Total number of folders deleted: {folders_deleted}")
