import os
import json
from tqdm import tqdm
from sha256 import sha256_checksum
import colorizer

def get_folder_size(path: str) -> int:
    """Calculate the total size of a folder in bytes."""

    total = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.isfile(fp):  # skip broken file links
                total += os.path.getsize(fp)
    return total

def linkr_compressor(package_name, folder_path, server_urls: list):
    """Compress a folder into a .linkr file with download links."""

    with open(package_name+'.linkr', 'w') as f, tqdm(total=get_folder_size(folder_path), unit='B', unit_scale=True, desc="Creating .linkr file", leave=True) as pbar:

        # Initialize the final data structure
        final_data = {
            "PACKAGE": package_name,
            "TOTAL_SIZE": get_folder_size(folder_path),
            "FILES": []
        }

        # Walk through the folder and gather file info
        for root, _, files in os.walk(folder_path):

            # Process each file
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, folder_path).replace('\\', '/')

                # Create download links for each server URL
                download_links = [f"{server_url}/{relative_path}" for server_url in server_urls]

                # Update progress bar
                file_size = os.path.getsize(file_path)
                pbar.update(file_size)

                # Create file info dictionary
                file_info = {
                    "URLS": download_links,
                    "DESTINATION": relative_path,
                    "SIZE": file_size,
                    "CHECKSUM": sha256_checksum(file_path)
                }
                final_data["FILES"].append(file_info)

        # Write the final data to the .linkr file in JSON format
        json.dump(final_data, f, indent=4)
    colorizer.success(f"Created {package_name}.linkr with {len(final_data['FILES'])} files.")