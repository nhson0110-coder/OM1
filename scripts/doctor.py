import sys
import platform
import shutil
import urllib.request
import os

def print_status(check_name, status, message=""):
    """Prints a colored status message to the console."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'
    
    if status:
        print(f"[{GREEN}PASS{RESET}] {check_name}")
    else:
        print(f"[{RED}FAIL{RESET}] {check_name} - {message}")

def check_python_version():
    """Checks if the Python version is 3.10 or higher."""
    major, minor, micro, release, serial = sys.version_info
    if major == 3 and minor >= 10:
        return True, f"{major}.{minor}.{micro}"
    return False, f"Current version: {major}.{minor}.{micro} (Required: 3.10+)"

def check_disk_space():
    """Checks for available disk space (requires at least 2GB)."""
    total, used, free = shutil.disk_usage("/")
    free_gb = free // (2**30)
    if free_gb > 2:
        return True, f"{free_gb} GB free"
    return False, f"Only {free_gb} GB free. AI models need space!"

def check_internet():
    """Checks internet connectivity by reaching GitHub."""
    try:
        urllib.request.urlopen('https://github.com', timeout=3)
        return True, "Connected"
    except:
        return False, "No internet connection"

def main():
    print("="*40)
    print(" 🚑 OM1 SYSTEM DOCTOR - HEALTH CHECK")
    print("="*40)
    
    # 1. Check OS
    print(f"OS Info: {platform.system()} {platform.release()} ({platform.machine()})")
    
    # 2. Check Python
    status, msg = check_python_version()
    print_status("Python Version (3.10+)", status, msg)
    
    # 3. Check Disk
    status, msg = check_disk_space()
    print_status("Disk Space (>2GB)", status, msg)
    
    # 4. Check Internet
    status, msg = check_internet()
    print_status("GitHub Connection", status, msg)

    print("\n✅ Diagnostic finished.")

if __name__ == "__main__":
    main()
