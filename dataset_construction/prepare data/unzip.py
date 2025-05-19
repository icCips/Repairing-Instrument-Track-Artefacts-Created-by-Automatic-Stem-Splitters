# script to unzip zips

import os
import zipfile

# Define paths
zip_dir = '/Volumes/Bank 1/FYP/Dataset/raw_zips'
output_dir = '/Volumes/Bank 1/FYP/Dataset/raw_unzipped'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Get list of all zip files in the directory
zip_files = [f for f in os.listdir(zip_dir) if f.endswith('.zip')]

total_files = len(zip_files)

# Iterate through each zip file
for index, filename in enumerate(zip_files, start=1):
    zip_path = os.path.join(zip_dir, filename)
    folder_name = os.path.splitext(filename)[0]
    output_subfolder = os.path.join(output_dir, folder_name)
    
    # Check if the folder already exists and is not empty
    if os.path.exists(output_subfolder) and os.listdir(output_subfolder):
        print(f'Skipped {index}/{total_files}: {filename} (Already extracted)')
        continue
    
    # Ensure the subfolder for unzipping exists
    os.makedirs(output_subfolder, exist_ok=True)
    
    try:
        # Unzip the file into the designated subfolder
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(output_subfolder)
        
        print(f'Extracted {index}/{total_files}: {filename} to {output_subfolder}')
    except zipfile.BadZipFile:
        print(f'Skipped {index}/{total_files}: {filename} (Bad Zip File)')

print("All files have been successfully processed.")
