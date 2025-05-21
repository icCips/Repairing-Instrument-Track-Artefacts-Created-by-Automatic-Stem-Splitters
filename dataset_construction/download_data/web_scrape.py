# Script to download multitrack zips

import requests
from bs4 import BeautifulSoup
import os
import time
from tqdm import tqdm

def download_file(url, folder, index, total):
    local_filename = url.split('/')[-1]
    
    if not os.path.exists(folder):
        os.makedirs(folder)

    full_path = os.path.join(folder, local_filename)

    if os.path.exists(full_path):
        tqdm.write(f"File already exists, skipping {index}/{total}: {local_filename}")
        return full_path

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total_size = int(r.headers.get('content-length', 0))
        chunk_size = 8192
        with open(full_path, 'wb') as f, tqdm(
            desc=f"Downloading {index}/{total}",
            total=total_size,
            unit='iB',
            unit_scale=True,
            dynamic_ncols=True,
            leave=True
        ) as bar:
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)
                bar.update(len(chunk))
    return full_path

def download(dataset_folder):
    
    download_folder = os.path.join(dataset_folder, "raw_zips")
    
    # multitrack page url
    base_url = "https://www.cambridge-mt.com/ms/mtk/"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    links = soup.find_all('a', href=True)

    download_links = []
    for link in links:
        href = link['href']
        if 'Full.zip' in href:
            if href.startswith('http'):
                download_links.append(href)
            else:
                download_links.append(requests.compat.urljoin(base_url, href))

    #download_folder = "/Volumes/Bank 1/FYP/Dataset/raw_zips"

    rate_limit_seconds = 2

    total_files = len(download_links)
    for index, link in enumerate(download_links, start=1):
        try:
            tqdm.write(f"\nProcessing {index}/{total_files}: {link}")
            download_file(link, download_folder, index, total_files)
            tqdm.write(f"Finished processing {index}/{total_files}: {link}")
        except Exception as e:
            tqdm.write(f"Failed to process {index}/{total_files}: {link}: {e}")
        time.sleep(rate_limit_seconds)

    print("Download completed.")
