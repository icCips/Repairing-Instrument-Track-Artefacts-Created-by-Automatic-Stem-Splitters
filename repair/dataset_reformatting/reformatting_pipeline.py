from dataset_generation import generate_dataset
from split_mono import check_dataset, split_all
from chunking import resample_and_chunk
from remove_short_file import remove_short_files
from remove_silence import remove_silent_files
from keep_high_sdr import keep_hi_sdr_files
from validate import validate

# sdr_filt recomendations for 12.5k files:
# vocal: 6
# bass: 9
# drums: 0
# other: 3

def pipeline(input, dataset, _16kHz_dataset, type, sdr_flt=0):

    # Generate the dataset
    generate_dataset(input, dataset, type)

    # Split mono
    files_to_split = check_dataset(dataset)

    split_all(files_to_split)

    # Resample and chunk the dataset
    resample_and_chunk(dataset, _16kHz_dataset)

    # Remove short files
    remove_short_files(_16kHz_dataset)

    # Remove silent files
    remove_silent_files(_16kHz_dataset)

    # Validate the dataset
    validate(_16kHz_dataset)

    # Keep high SDR files
    keep_hi_sdr_files(_16kHz_dataset, sdr_flt)

    # Validate the dataset
    validate(_16kHz_dataset)

pipeline("CMS_MixR_U", "CMS_MixR_U_bass_16kHz", "CMS_MixR_U_bass_16kHz_5s_chunks", "bass", 9)
pipeline("CMS_MixR_U", "CMS_MixR_U_vocal_16kHz", "CMS_MixR_U_vocal_16kHz_5s_chunks", "vocal", 6)
pipeline("CMS_MixR_U", "CMS_MixR_U_drums_16kHz", "CMS_MixR_U_drums_16kHz_5s_chunks", "drums", 0)
pipeline("CMS_MixR_U", "CMS_MixR_U_other_16kHz", "CMS_MixR_U_other_16kHz_5s_chunks", "other", 3)
