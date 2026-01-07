import tkinter as tk
import sys
import ctypes
import os
from os_utility_tool.gui import OSUtilityApp
from os_utility_tool.os_detector import is_windows

def is_admin():
    """
    Checks if the current process has administrative privileges.
    """
    try:
        if is_windows():
            return ctypes.windll.shell32.IsUserAnAdmin()
        else:
            return os.getuid() == 0
    except AttributeError:
        return False

def main():
    # Attempt to notify user if not admin
    if not is_admin():
        print("Warning: Some features may require Administrative/Root privileges.")
    
    root = tk.Tk()
    
    # Set icon if available, or just title
    root.title("OS Utility Tool v1.0")
    
    # Initialize the app
    app = OSUtilityApp(root)
    
    # Run
    root.mainloop()

if __name__ == "__main__":
    main()
