from os_utility_tool.os_detector import is_windows
from os_utility_tool.utils.command_runner import run_command
import os

def analyze_home_directory():
    """
    Analyzes size of folders in the user's home directory.
    """
    if is_windows():
        cmd = 'Get-ChildItem $HOME | Where-Object { $_.PSIsContainer } | Select-Object Name, @{N=\'Size(MB)\';E={ (Get-ChildItem $_.FullName -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB -as [int] }} | Sort-Object \'Size(MB)\' -Descending | Out-String'
    else:
        # Linux implementation: du -sh for top level items, sorted by size
        cmd = 'echo "Top 10 items in home directory:"; du -sh ~/* 2>/dev/null | sort -rh | head -n 10'

    success, output = run_command(cmd)
    return output if success else f"Error: {output}"
