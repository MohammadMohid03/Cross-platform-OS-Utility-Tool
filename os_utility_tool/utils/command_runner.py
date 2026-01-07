import subprocess
import os
from os_utility_tool.os_detector import is_windows

def run_command(command, use_shell=True):
    """
    Executes a system command and returns the output or error.
    On Windows, it uses PowerShell if possible for modern scripting.
    On Linux, it uses the default shell (Bash).
    """
    try:
        # On Windows, we prefer running commands through powershell for better consistency with system tasks
        if is_windows():
            # Use a list to avoid shell quoting issues
            full_command = ["powershell", "-ExecutionPolicy", "Bypass", "-Command", command]
            is_shell = False
        else:
            full_command = command
            is_shell = True

        process = subprocess.Popen(
            full_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=is_shell,
            text=True
        )
        
        stdout, stderr = process.communicate()
        
        if process.returncode == 0:
            return True, stdout
        else:
            return False, stderr or stdout
            
    except Exception as e:
        return False, str(e)

def run_gui_command(command):
    """
    Variation that might be used for commands that need to run in background
    without blocking the GUI, but simplified for this utility.
    """
    return run_command(command)
