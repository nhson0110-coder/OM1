"""
System health check script for OM1.

This script performs diagnostic checks for:
- Python version compatibility
- Available disk space
- Internet connectivity to GitHub
"""

import platform
import shutil
import sys
import urllib.request
from typing import Tuple


def print_status(check_name: str, status: bool, message: str = "") -> None:
    """
    Print a colored status message to the console.

    Args:
        check_name: The name of the check being performed.
        status: True if the check passed, False otherwise.
        message: Additional details about the check result.
    """
    green = "\033[92m"
    red = "\033[91m"
    reset = "\033[0m"

    if status:
        print(f"[{green}PASS{reset}] {check_name}")
    else:
        print(f"[{red}FAIL{reset}] {check_name} - {message}")


def check_python_version() -> Tuple[bool, str]:
    """
    Check if the Python version is 3.10 or higher.

    Returns:
        Tuple[bool, str]: Status and version string/message.
    """
    major, minor, micro = sys.version_info[:3]
    if major == 3 and minor >= 10:
        return True, f"{major}.{minor}.{micro}"
    return False, f"Current: {major}.{minor}.{micro} (Req: 3.10+)"


def check_disk_space() -> Tuple[bool, str]:
    """
    Check for available disk space (requires at least 2GB).

    Returns:
        Tuple[bool, str]: Status and space info.
    """
    # Use underscores for unused variables to satisfy linter
    _, _, free = shutil.disk_usage("/")
    free_gb = free // (2**30)
    if free_gb > 2:
        return True, f"{free_gb} GB free"
    return False, f"Only {free_gb} GB free. AI models need space!"


def check_internet() -> Tuple[bool, str]:
    """
    Check internet connectivity by reaching GitHub.

    Returns:
        Tuple[bool, str]: Status and connection info.
    """
    try:
        with urllib.request.urlopen("https://github.com", timeout=3):
            return True, "Connected"
    except Exception:  # pylint: disable=broad-except
        return False, "No internet connection"


def main() -> None:
    """Run all diagnostic checks."""
    print("=" * 40)
    print(" 🚑 OM1 SYSTEM DOCTOR - HEALTH CHECK")
    print("=" * 40)

    # 1. Check OS
    os_info = f"{platform.system()} {platform.release()} ({platform.machine()})"
    print(f"OS Info: {os_info}")

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
