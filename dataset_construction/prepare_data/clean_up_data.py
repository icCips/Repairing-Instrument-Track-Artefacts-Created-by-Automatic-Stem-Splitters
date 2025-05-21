import os
import shutil
from pathlib import Path

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

def clean(dataset_path):
    
    print("Cleaning up data...")
    
    base_dir = os.path.join(dataset_path, "raw_unzipped")

    folders_deleted = 0

    for batch_folder in os.listdir(base_dir):
        batch_folder_path = os.path.join(base_dir, batch_folder)
        
        if os.path.isdir(batch_folder_path):

            for mix_folder in os.listdir(batch_folder_path):
                mix_folder_path = os.path.join(batch_folder_path, mix_folder)
                
                if os.path.isdir(mix_folder_path):

                    has_wav_or_flac = find_and_move_wav_files(mix_folder_path, mix_folder_path)
                    
                    if not has_wav_or_flac:

                        shutil.rmtree(mix_folder_path)
                        folders_deleted += 1
                        print(f"Deleted folder without .wav or .flac file: {mix_folder_path}")
                    else:

                        delete_non_wav_flac_files(mix_folder_path)
                        
                        delete_subfolders(mix_folder_path)
                        
                        print(f"Moved files, deleted non-wav/flac files, and cleaned up folder: {mix_folder_path}")

    print(f"Total number of folders deleted: {folders_deleted}")

def delete_zips(dataset_path):

    folder_path = os.path.join(dataset_path, "raw_zips")

    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(f"Deleted: {folder_path}")
    else:
        print(f"Folder not found: {folder_path}")

def delete_raw_unzipped(dataset_path):
    folder_path = os.path.join(dataset_path, "raw_unzipped")

    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(f"Deleted: {folder_path}")
    else:
        print(f"Folder not found: {folder_path}")
        
def collapse(dataset_path):

    base_dir = Path(dataset_path)
    src_dir = base_dir / "generated_mixes"

    # Move all files and directories from generated_mixes to CMS_MixR_U
    for item in src_dir.iterdir():
        dest = base_dir / item.name
        if dest.exists():
            print(f"Skipping {item.name}, already exists in destination.")
        else:
            shutil.move(str(item), str(dest))

    # Delete the now-empty generated_mixes folder
    if not any(src_dir.iterdir()):
        src_dir.rmdir()
        print("Removed empty 'generated_mixes' folder.")
    else:
        print("'generated_mixes' not empty; manual cleanup may be needed.")






