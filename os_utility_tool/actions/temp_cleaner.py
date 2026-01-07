from os_utility_tool.os_detector import is_windows
from os_utility_tool.utils.command_runner import run_command

def clean_temp_files():
    """
    Deletes temporary system and user files.
    Demonstrates: File system operations, OS Abstraction.
    """
    if is_windows():
        # Clean User Temp and System Temp
        cmd = 'Remove-Item -Path "$env:TEMP\*" -Recurse -Force -Confirm:$false -ErrorAction SilentlyContinue; ' \
              'Remove-Item -Path "C:\Windows\Temp\*" -Recurse -Force -Confirm:$false -ErrorAction SilentlyContinue'
    else:
        # Linux implementation (Bash)
        cmd = 'echo "Cleaning /tmp..."; rm -rf /tmp/* 2>/dev/null; ' \
              'echo "Cleaning user cache..."; rm -rf ~/.cache/* 2>/dev/null; ' \
              'echo "Cleanup task finished."'

    success, output = run_command(cmd)
    if success:
        return "Cleanup completed successfully. (Some files might be in use and were skipped)"
    else:
        return f"Error during cleanup: {output}"
