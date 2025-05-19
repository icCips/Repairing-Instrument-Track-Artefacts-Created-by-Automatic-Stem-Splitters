import os
import shutil

# Path to the main folder containing all subfolders
main_folder_path = "/Volumes/Bank 1/FYP/Dataset/raw_unzipped"

# List all subfolders in the main folder
subfolders = [f for f in os.listdir(main_folder_path) if os.path.isdir(os.path.join(main_folder_path, f))]

# Sort subfolders to ensure consistent ordering
subfolders.sort()

# Number of subfolders per batch
batch_size = 60

# Total number of batches
total_batches = (len(subfolders) + batch_size - 1) // batch_size
print(f"Total subfolders: {len(subfolders)}")
print(f"Number of batches to create: {total_batches}")

# Split subfolders into batches
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
