from download_data.web_scrape import download

from prepare_data.unzip import extract_zip
from prepare_data.batch import batch
from prepare_data.clean_up_data import clean, delete_zips, delete_raw_unzipped, collapse
from prepare_data.group import group_files

from MixR.generate_mixes import generate_mixes

from Wave_U_Net_Pytorch.iterate import seperate_dataset

# Warning: this code takes a long time to run. Consider running one function at a time.

# Download and preprocessing

dataset_path = "CMS_MixR_U"

download(dataset_path)

extract_zip(dataset_path)

batch(dataset_path)

clean(dataset_path)

group_files(dataset_path)

delete_zips(dataset_path)

# Data augmentation

generate_mixes("ver_1", dataset_path)
generate_mixes("ver_2", dataset_path)
generate_mixes("ver_3", dataset_path)
generate_mixes("ver_4", dataset_path)
generate_mixes("ver_5", dataset_path)
generate_mixes("ver_6", dataset_path)
generate_mixes("ver_7", dataset_path)
generate_mixes("ver_8", dataset_path)
generate_mixes("ver_9", dataset_path)
generate_mixes("ver_10", dataset_path)

# Noisy data generation

seperate_dataset(dataset_path)

delete_raw_unzipped(dataset_path)

collapse(dataset_path)