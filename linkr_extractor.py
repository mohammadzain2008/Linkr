import os
import json
import requests
from resource_downloader import download_stream
import colorizer
from sha256 import sha256_checksum
import hashlib
from urllib.parse import urlparse

def linkr_extractor(file_path, folder_path, checksum_override=False, integrity_check=True):
    """Extract files from a .linkr file to the specified folder."""

    if not os.path.isfile(file_path):
        colorizer.error(f"The linkr file '{file_path}' does not exist.")
        print(f"[STD_CODE] 101")
        return 101

    failed_downloads = []
    corrupted_files = []

    with open(file_path, 'r') as f:
        data = json.load(f)

    package_name = data.get("PACKAGE", "UnknownPackage")
    files = data.get("FILES", [])
    file_count = len(files)
    total_size = data.get("TOTAL_SIZE", 0) / (1024 * 1024)  # Convert to MB
    linkr_address = data.get("LINKR_ADDRESS", [])

    linkr_checksum = sha256_checksum(file_path)
    for address in linkr_address:

        try:
            response = requests.get(address)

            if response.status_code == 200:
                sha256_hash = hashlib.sha256()

                for chunk in response.iter_content(chunk_size=8192):
                    sha256_hash.update(chunk)
                
                remote_checksum = sha256_hash.hexdigest()
                
                if remote_checksum == linkr_checksum:
                    colorizer.success(f"Verified .linkr file with server at {address}")
                
                else:
                    colorizer.error(f"Checksum mismatch with server at {address}. Expected {linkr_checksum}, got {remote_checksum}")
                    colorizer.error("Aborting extraction due to checksum mismatch. Your .linkr file may have been tampered with which puts your system at a risk!")
                    print(f"[STD_CODE] 200")
                    return 200
            
            if response.status_code == 404:
                colorizer.warning(f"{package_name}.linkr file not found on server at {address}.")
                colorizer.warning(f"Could not verify integrity of {package_name}.linkr file.")
                
                if integrity_check == True:
                    colorizer.error("Aborting extraction.")
                    print(f"[STD_CODE] 201")
                    return 201

        except Exception as e:
            colorizer.warning(f"Could not verify .linkr file with server at {address}: {e}")

    for file_info in files:
        urls = file_info.get("URLS", [])
        destination = file_info.get("DESTINATION", "")
        size = file_info.get("SIZE", 0)
        expected_checksum = file_info.get("CHECKSUM", "")

        fail_count = 0
        for url in urls:
            parsed_url = urlparse(url)
            domain = f"{parsed_url.scheme}://{parsed_url.netloc}"

            try:
                requests.get(domain, timeout=5)

            except Exception as e:
                colorizer.warning(f"Could not reach server at {domain}: {e}")
                urls.remove(url)

        if len(urls) == 0:
            colorizer.error(f"No reachable URLs for {destination}. Skipping download.")
            fail_count += 1
            failed_downloads.append(destination)
    
        if fail_count == file_count:
            colorizer.error("All download URLs are unreachable. Aborting extraction.")
            print(f"[STD_CODE] 300")
            return 300
        
        colorizer.info(f"\nExtracting package: {package_name} with {len(files)} files.")
        colorizer.info(f"Package size: {total_size:.4f} MB\n")
        
        dest_path = os.path.join(folder_path, destination)
        dest_dir = os.path.dirname(dest_path)

        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        colorizer.info(f"Downloading {destination}...")
        actual_checksum = download_stream(urls, dest_path)

        if not actual_checksum:
            colorizer.error(f"Failed to download {destination}.")
            failed_downloads.append(destination)
            continue

        if actual_checksum != expected_checksum:
            corrupted_files.append(destination)

            if checksum_override:
                colorizer.warning(f"Checksum mismatch for {destination}, but overriding as per user request.")
            else:
                colorizer.error(f"Checksum mismatch for {destination}. Expected {expected_checksum}, got {actual_checksum}. Deleting corrupted file.")
                os.remove(dest_path)
                continue
        else:
            colorizer.success(f"Successfully downloaded and verified {destination}.")

    if failed_downloads:
        colorizer.error(f"\nFailed to download {len(failed_downloads)} files:", header=False)
        for file in failed_downloads:
            colorizer.error(f"- {file}", header=False)

    if corrupted_files:
        colorizer.error(f"\nCorrupted files found:", header=False)
        for file in corrupted_files:
            colorizer.error(f"- {file}", header=False)

    colorizer.success(f"\nExtraction of package '{package_name}' completed.", header=False)
    print(f"[STD_CODE] 0")
    return 0