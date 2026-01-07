from os_utility_tool.os_detector import is_windows
from os_utility_tool.utils.command_runner import run_command

def get_disk_usage():
    """
    Displays disk usage information.
    Demonstrates: System calls, Data parsing.
    """
    if is_windows():
        # Get-PSDrive provides a clean summary of drives
        cmd = 'Get-PSDrive -PSProvider FileSystem | Select-Object Name, @{N=\'Used(GB)\';E={[math]::round($_.Used/1GB,2)}}, @{N=\'Free(GB)\';E={[math]::round($_.Free/1GB,2)}}, @{N=\'Total(GB)\';E={[math]::round(($_.Used+$_.Free)/1GB,2)}} | Out-String'
    else:
        # Linux implementation: Filter for physical disks and format nicely
        cmd = 'df -h --output=source,fstype,size,used,avail,pcent,target -x tmpfs -x devtmpfs'

    success, output = run_command(cmd)
    return output if success else f"Error: {output}"

def list_root_files():
    """
    Lists files in the root directory.
    """
    if is_windows():
        cmd = 'Get-ChildItem -Path C:\ | Select-Object Name, LastWriteTime, Length | Out-String'
    else:
        cmd = 'ls -lHA /'
        
    success, output = run_command(cmd)
    return output if success else f"Error: {output}"
