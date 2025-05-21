import os
import zipfile

def extract_zip(dataset_folder):
    print("Extracting zip files...")
    
    zip_dir = os.path.join(dataset_folder, "raw_zips")
    output_dir = os.path.join(dataset_folder, "raw_unzipped")

    os.makedirs(output_dir, exist_ok=True)

    zip_files = [f for f in os.listdir(zip_dir) if f.endswith('.zip')]

    total_files = len(zip_files)

    for index, filename in enumerate(zip_files, start=1):
        zip_path = os.path.join(zip_dir, filename)
        folder_name = os.path.splitext(filename)[0]
        output_subfolder = os.path.join(output_dir, folder_name)
        
        if os.path.exists(output_subfolder) and os.listdir(output_subfolder):
            print(f'Skipped {index}/{total_files}: {filename} (Already extracted)')
            continue
        
        os.makedirs(output_subfolder, exist_ok=True)
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(output_subfolder)
            
            print(f'Extracted {index}/{total_files}: {filename} to {output_subfolder}')
        except zipfile.BadZipFile:
            print(f'Skipped {index}/{total_files}: {filename} (Bad Zip File)')

    print("All files have been extracted.")
