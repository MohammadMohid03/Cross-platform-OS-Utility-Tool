from os_utility_tool.os_detector import is_windows
from os_utility_tool.utils.command_runner import run_command

def get_system_info():
    """
    Displays OS name, version, CPU info, and RAM info.
    Demonstrates: System information retrieval.
    """
    if is_windows():
        cmd = 'Write-Output "--- OS Info ---"; Get-ComputerInfo | Select-Object OsName, OsVersion, OsArchitecture | Out-String; ' \
              'Write-Output "--- CPU Info ---"; Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores | Out-String; ' \
              'Write-Output "--- RAM Info ---"; Get-CimInstance Win32_PhysicalMemory | Measure-Object -Property Capacity -Sum | Select-Object @{N="Total RAM (GB)";E={$_.Sum / 1GB}} | Out-String'
    else:
        cmd = 'echo "--- OS Info ---"; uname -a; ' \
              'echo "\n--- CPU Info ---"; lscpu | grep "Model name"; ' \
              'echo "\n--- RAM Info ---"; free -h'

    success, output = run_command(cmd)
    return output if success else f"Error: {output}"
