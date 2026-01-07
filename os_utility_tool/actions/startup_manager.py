from os_utility_tool.os_detector import is_windows
from os_utility_tool.utils.command_runner import run_command

def list_startup_programs():
    """
    Displays startup applications.
    Demonstrates: OS-specific configuration reading.
    """
    if is_windows():
        cmd = 'Get-CimInstance Win32_StartupCommand | Select-Object Name, Command, User | Out-String'
    else:
        # Check XDG autostart on Linux - checking directory existence first to avoid non-zero exit codes
        cmd = 'echo "--- System Autostart ---"; [ -d /etc/xdg/autostart ] && find /etc/xdg/autostart/ -name "*.desktop" -exec basename {} \; 2>/dev/null; ' \
              'echo "\n--- User Autostart ---"; [ -d ~/.config/autostart ] && find ~/.config/autostart/ -name "*.desktop" -exec basename {} \; 2>/dev/null; ' \
              'exit 0'

    success, output = run_command(cmd)
    return output if success else f"Error: {output}"
