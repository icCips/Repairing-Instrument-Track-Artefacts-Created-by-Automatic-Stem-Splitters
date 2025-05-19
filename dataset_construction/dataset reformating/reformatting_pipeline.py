from dataset_generation import generate_dataset
from split_mono import check_dataset, split_all
from chunking import resample_and_chunk
from remove_short_file import remove_short_files
from remove_silence import remove_silent_files
from keep_high_sdr import keep_hi_sdr_files
from validate import validate

#voice sdr = 1

input = "/Volumes/Bank_1/FYP/Dataset/generated_mixes"
dataset = "/Volumes/Bank_1/FYP/Dataset/sgmse_bass"
_16kHz_dataset = "/Volumes/Bank_1/FYP/Dataset/sgmse_bass_16kHz_5s_chunks"
type = "bass"

# Generate the dataset
#generate_dataset(input, dataset, type)

# Split mono
#files_to_split = check_dataset(dataset)

#split_all(files_to_split)

# Resample and chunk the dataset
#resample_and_chunk(dataset, _16kHz_dataset)

# Remove short files
#remove_short_files(_16kHz_dataset)

# Remove silent files
#remove_silent_files(_16kHz_dataset)

# Validate the dataset
#validate(_16kHz_dataset)

# Keep high SDR files
#keep_hi_sdr_files(_16kHz_dataset, 9)

# Validate the dataset
#validate(_16kHz_dataset)


input = "/Volumes/Bank_1/FYP/Dataset/generated_mixes"
dataset = "/Volumes/Bank_1/FYP/Dataset/sgmse_drums"
_16kHz_dataset = "/Volumes/Bank_1/FYP/Dataset/sgmse_drums_16kHz_5s_chunks"
type = "drums"

# Generate the dataset
#generate_dataset(input, dataset, type)

# Split mono
#files_to_split = check_dataset(dataset)

#split_all(files_to_split)

# Resample and chunk the dataset
#resample_and_chunk(dataset, _16kHz_dataset)

# Remove short files
#remove_short_files(_16kHz_dataset)

# Remove silent files
#remove_silent_files(_16kHz_dataset)

# Validate the dataset
#validate(_16kHz_dataset)

# Keep high SDR files
#keep_hi_sdr_files(_16kHz_dataset, 0)

# Validate the dataset
#validate(_16kHz_dataset)

input = "/Volumes/Bank_1/FYP/Dataset/generated_mixes"
dataset = "/Volumes/Bank_1/FYP/Dataset/sgmse_other"
_16kHz_dataset = "/Volumes/Bank_1/FYP/Dataset/sgmse_other_16kHz_5s_chunks"
type = "other"

# Generate the dataset
#generate_dataset(input, dataset, type)

# Split mono
#files_to_split = check_dataset(dataset)

#split_all(files_to_split)

# Resample and chunk the dataset
#resample_and_chunk(dataset, _16kHz_dataset)

# Remove short files
#remove_short_files(_16kHz_dataset)

# Remove silent files
#remove_silent_files(_16kHz_dataset)

# Validate the dataset
validate(_16kHz_dataset)

# Keep high SDR files
keep_hi_sdr_files(_16kHz_dataset, 3)

# Validate the dataset
validate(_16kHz_dataset)

