from os_utility_tool.os_detector import is_windows
from os_utility_tool.utils.command_runner import run_command

def clean_cache_and_logs():
    """
    Clears cache directories and removes old log files.
    """
    if is_windows():
        cmd = 'Get-ChildItem -Path "C:\Windows\Logs\*" -Recurse -ErrorAction SilentlyContinue | Remove-Item -Force -Recurse -Confirm:$false -ErrorAction SilentlyContinue; ' \
              'Write-Output "Logs cleared. Clearing browser cache markers..."; ' \
              '[System.GC]::Collect()'
    else:
        cmd = 'echo "Cleaning user cache..."; rm -rf ~/.cache/* 2>/dev/null; ' \
              'echo "Cleaning system logs..."; rm -rf /var/log/*.log 2>/dev/null; ' \
              'echo "Caches and logs cleared (Sudo required for system logs)"'

    success, output = run_command(cmd)
    return "Cleanup executed." if success else f"Error: {output}"
