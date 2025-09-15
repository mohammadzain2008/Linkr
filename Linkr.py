from linkr_compressor import linkr_compressor
from linkr_extractor import linkr_extractor
import sys

if __name__ == "__main__":
    
    if len(sys.argv) < 3:
        print("Usage: linkr <compress/extract> <arguments>")
        sys.exit(1)
    
    command = sys.argv[1]

    if command == "compress":
        package_name = sys.argv[2]
        folder_path = sys.argv[3]
        server_urls = sys.argv[4:]
        linkr_compressor(package_name, folder_path, server_urls)

    elif command == "extract":
        file_path = sys.argv[2]
        folder_path = sys.argv[3]
        checksum_override = '--override-checksum' in sys.argv
        linkr_extractor(file_path, folder_path, checksum_override)