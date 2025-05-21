import os
import shutil

def batch (dataset_folder):

    print("Batching data...")
    
    main_folder_path = os.path.join(dataset_folder, "raw_unzipped")

    subfolders = [f for f in os.listdir(main_folder_path) if os.path.isdir(os.path.join(main_folder_path, f))]

    subfolders.sort()

    batch_size = 60

    total_batches = (len(subfolders) + batch_size - 1) // batch_size
    print(f"Total subfolders: {len(subfolders)}")
    print(f"Number of batches to create: {total_batches}")

    for i in range(0, len(subfolders), batch_size):
        batch = subfolders[i:i + batch_size]
        
        # Create a new folder for the current batch
        batch_number = i // batch_size + 1
        batch_folder_name = f"batch_{batch_number}"
        batch_folder_path = os.path.join(main_folder_path, batch_folder_name)
        os.makedirs(batch_folder_path, exist_ok=True)
        
        print(f"\nCreating {batch_folder_name} with {len(batch)} subfolders...")

        # Move each subfolder in the current batch to the new batch folder
        for subfolder in batch:
            source = os.path.join(main_folder_path, subfolder)
            destination = os.path.join(batch_folder_path, subfolder)
            shutil.move(source, destination)
            print(f"  Moved subfolder: {subfolder}")
        
        print(f"{batch_folder_name} created successfully.")

    print("\nAll subfolders have been successfully split into batches.")
