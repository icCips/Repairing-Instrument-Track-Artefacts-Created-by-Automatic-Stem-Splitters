# Script to download multitrack zips

import requests
from bs4 import BeautifulSoup
import os
import time
from tqdm import tqdm

# Function to download a file from a URL with a progress bar
def download_file(url, folder, index, total):
    local_filename = url.split('/')[-1]
    # Create local folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)
    # Full path for saving the file
    full_path = os.path.join(folder, local_filename)
    
    # Check if the file already exists
    if os.path.exists(full_path):
        tqdm.write(f"File already exists, skipping {index}/{total}: {local_filename}")
        return full_path

    # Start the download
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total_size = int(r.headers.get('content-length', 0))
        chunk_size = 8192
        with open(full_path, 'wb') as f, tqdm(
            desc=f"Downloading {index}/{total}",
            total=total_size,
            unit='iB',
            unit_scale=True,
            dynamic_ncols=True,  # Automatically adjust progress bar width
            leave=True  # Ensure progress bar remains until next iteration
        ) as bar:
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)
                bar.update(len(chunk))
    return full_path

# URL of the multitrack page
base_url = "https://www.cambridge-mt.com/ms/mtk/"
response = requests.get(base_url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find all download links
links = soup.find_all('a', href=True)

# Filter out the links that are for multitrack downloads
download_links = []
for link in links:
    href = link['href']
    if 'Full.zip' in href:
        # If the link is already absolute, use it directly
        if href.startswith('http'):
            download_links.append(href)
        else:
            # Otherwise, construct the full URL
            download_links.append(requests.compat.urljoin(base_url, href))

# Base folder to save downloads
download_folder = "/Volumes/Bank 1/FYP/Dataset/raw_zips"

# Rate limit configuration
rate_limit_seconds = 2  # Time to wait between downloads in seconds

# Download each file with rate limiting
total_files = len(download_links)
for index, link in enumerate(download_links, start=1):
    try:
        tqdm.write(f"\nProcessing {index}/{total_files}: {link}")
        download_file(link, download_folder, index, total_files)
        tqdm.write(f"Finished processing {index}/{total_files}: {link}")
    except Exception as e:
        tqdm.write(f"Failed to process {index}/{total_files}: {link}: {e}")
    # Wait before the next download to respect rate limit
    time.sleep(rate_limit_seconds)

print("Download completed.")
