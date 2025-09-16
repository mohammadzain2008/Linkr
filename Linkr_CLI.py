from linkr_compressor import linkr_compressor
from linkr_extractor import linkr_extractor

from global_var import CLI_VERSION as VERSION

print("="*50)
print(f"Linkr v{VERSION}!")
print("Linkr is a tool to package folders into .linkr files with download links, and extract them later.")
print("For more information, visit: https://github.com/mohammadzain2008/Linkr")
print("="*50)
print()
print("1. Create a .linkr file from a folder")
print("2. Extract files from a .linkr file")
choice = input("Enter your choice (1 or 2): ")

if choice == '1':
    package_name = input("Enter the package name (without .linkr extension): ")
    folder_path = input("Enter the path to the folder to be packaged: ")
    server_urls = input("Enter server URLs (comma-separated): ").split(',')
    server_urls = [url.strip().rstrip('/') for url in server_urls if url.strip()]
    
    if not server_urls:
        print("Error: At least one valid server URL is required.")
    else:
        linkr_compressor(package_name, folder_path, server_urls)

elif choice == '2':
    file_path = input("Enter the path to the .linkr file: ")
    folder_path = input("Enter the path to the folder where files should be extracted: ")
    checksum_override = input("Override checksum errors? (y/n): ").strip().lower() == 'y'
    linkr_extractor(file_path, folder_path, checksum_override)

input("\nPress Enter to exit...")