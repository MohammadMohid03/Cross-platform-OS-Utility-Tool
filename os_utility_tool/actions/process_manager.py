from os_utility_tool.os_detector import is_windows
from os_utility_tool.utils.command_runner import run_command

def list_processes():
    """
    Lists all active processes with PID, Name, and Memory.
    Demonstrates: Process management.
    """
    if is_windows():
        # Sort by WorkingSet (physical memory) descending and pick top 20
        cmd = 'Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First 20 | ' \
              'Select-Object Id, ProcessName, @{N=\'Memory(MB)\';E={[math]::round($_.WorkingSet64/1MB,2)}}, ' \
              '@{N=\'CPU(%)\';E={if($_.CPU){$_.CPU}else{0}}} | Out-String'
    else:
        # ps aux on Linux
        cmd = 'ps aux --sort=-%mem | head -n 21'

    success, output = run_command(cmd)
    return output if success else f"Error: {output}"

def kill_process(pid):
    """
    Terminates a process by PID.
    """
    if not pid:
        return "Error: Please provide a PID."
        
    if is_windows():
        cmd = f'Stop-Process -Id {pid} -Force'
    else:
        cmd = f'kill -9 {pid}'

    success, output = run_command(cmd)
    if success:
        return f"Process {pid} terminated successfully."
    else:
        return f"Failed to terminate process {pid}: {output}"
