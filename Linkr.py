import requests
from pathlib import Path
import os
from tqdm import tqdm

def download_stream(url: str, dest_path: str, chunk_size: int = 8192, verify: bool = True):

    dest = Path(dest_path)
    dest.parent.mkdir(parents=True, exist_ok=True)

    # Write to a temporary file first
    tmp_path = dest.with_suffix(dest.suffix + '.part')

    with requests.get(url, stream=True, verify=verify) as r:

        r.raise_for_status()
        total_size = int(r.headers.get('content-length', 0))
        
        with open(tmp_path, 'wb') as f, tqdm(total=total_size, unit='iB', unit_scale=True, desc=str(dest), disable=(total_size == 0)) as pbar:
            
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))

    os.replace(tmp_path, dest)  # Atomic operation
    return dest

def linkr_compressor(folder, server, output_linkr):

    try:
        with open(output_linkr, 'w') as linkr_file:
            linkr_file.write(f"PKG_NAME:{os.path.basename(folder)}\n")
            for root, _, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    print(file_path)
                    url = f"{server}/{file_path.replace(os.sep, '/')}"
                    linkr_file.write(f"{url}::::{file_path}\n")
    except Exception as e:
        print(f"Error writing to file {output_linkr}: {e}")

def linkr_extractor(file_path, dest_folder):
    links = []
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line and not line.startswith('PKG_NAME:'):
                    parts = line.split('::::')
                    if len(parts) == 2:
                        url, path = parts
                        links.append((url.strip(), path.strip()))
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")

    for url, path in links:
        download_stream(url, dest_folder + '/' + path, verify=True)

print("--------------------------------")
print("Welcome to Linkr Engine")
print("--------------------------------")
print("1. Compress")
print("2. Extract")
choice = input("Enter your choice (1 or 2): ")
if choice == '1':
    folder = input("Enter the folder path to compress: ")
    server = input("Enter the server URL (e.g., http://127.0.0.1:8000): ")
    output_linkr = input("Enter the output .linkr file path: ")
    linkr_compressor(folder, server, output_linkr + '.linkr')

elif choice == '2':
    file_path = input("Enter the .linkr file path to extract: ")
    folder = input("Enter the destination folder path: ")
    if not os.path.exists(folder):
        os.makedirs(folder)
    linkr_extractor(file_path, folder)

input("Press Enter to exit...")