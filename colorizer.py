def error(message, header=True):
    if header:
        print(f"\033[91m[ERROR]: {message}\033[0m")  # Red color for errors
    else:
        print(f"\033[91m{message}\033[0m")  # Red color for errors without header

def info(message, header=True):
    if header:
        print(f"\033[94m[INFO]: {message}\033[0m")  # Blue color for info messages
    else:
        print(f"\033[94m{message}\033[0m")  # Blue color for info messages without header

def success(message, header=True):
    if header:
        print(f"\033[92m[SUCCESS]: {message}\033[0m")  # Green color for success messages
    else:
        print(f"\033[92m{message}\033[0m")  # Green color for success messages without header

def warning(message, header=True):
    if header:
        print(f"\033[93m[WARNING]: {message}\033[0m")  # Yellow color for warnings
    else:
        print(f"\033[93m{message}\033[0m")  # Yellow color for warnings without header