import platform

def get_os():
    """
    Detects the operating system.
    Returns 'Windows', 'Linux', or 'Unknown'.
    """
    system = platform.system()
    if system == "Windows":
        return "Windows"
    elif system == "Linux":
        return "Linux"
    else:
        return "Unknown"

def is_windows():
    return get_os() == "Windows"

def is_linux():
    return get_os() == "Linux"
