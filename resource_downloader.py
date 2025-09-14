from typing import List
from pathlib import Path
import requests, os
from tqdm import tqdm
from sha256 import sha256_checksum
import colorizer

def download_stream(urls: List[str], dest_path: str, chunk_size: int = 1024, verify: bool = True):
    """Download a file from a list of URLs with progress bar and also returns the SHA-256 checksum."""

    # Set headers to bypass ngrok browser warning (only if using ngrok)
    headers = {"ngrok-skip-browser-warning": "true"}

    dest = Path(dest_path)
    dest.parent.mkdir(parents=True, exist_ok=True)

    # Create a temporary file path
    tmp_path = dest.with_suffix(dest.suffix + '.part')

    last_exception = None

    # Try each URL in the list until one succeeds
    for url in urls:
        try:
            # Stream download with progress bar
            with requests.get(url, stream=True, verify=verify, timeout=(5, 15), headers=headers) as r:
                r.raise_for_status()
                total_size = int(r.headers.get('content-length', 0))

                # Download to a temporary file first
                with open(tmp_path, 'wb') as f, tqdm(total=total_size, unit='B', unit_scale=True, desc=str(dest), leave=False, position=0, disable=(total_size == 0)) as pbar:
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))

            # Move the temporary file to the final destination
            os.replace(tmp_path, dest)

            # Compute and return the checksum
            checksum = sha256_checksum(dest)
            return checksum
        
        except Exception as e:
            colorizer.warning(f"Failed to download from {url}. Trying any fallback URLs if available...")
            last_exception = e

    # If all URLs fail
    if last_exception:
        return False