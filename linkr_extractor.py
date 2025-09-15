import os
import json
from resource_downloader import download_stream
import colorizer

def linkr_extractor(file_path, folder_path, checksum_override=False):
    """Extract files from a .linkr file to the specified folder."""

    failed_downloads = []
    corrupted_files = []

    with open(file_path, 'r') as f:
        data = json.load(f)

    package_name = data.get("PACKAGE", "UnknownPackage")
    files = data.get("FILES", [])
    total_size = data.get("TOTAL_SIZE", 0) / (1024 * 1024)  # Convert to MB

    colorizer.info(f"\nExtracting package: {package_name} with {len(files)} files.")
    colorizer.info(f"Package size: {total_size:.2f} MB\n")

    for file_info in files:
        urls = file_info.get("URLS", [])
        destination = file_info.get("DESTINATION", "")
        size = file_info.get("SIZE", 0)
        expected_checksum = file_info.get("CHECKSUM", "")

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