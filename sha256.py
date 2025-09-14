import hashlib

def sha256_checksum(file_path: str, chunk_size: int = 8192) -> str:
    """Compute the SHA-256 checksum of a file."""

    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(chunk_size), b''):
            sha256.update(chunk)
    return sha256.hexdigest()