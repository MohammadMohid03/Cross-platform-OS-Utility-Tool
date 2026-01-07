from os_utility_tool.os_detector import is_windows
from os_utility_tool.utils.command_runner import run_command

def get_live_resources():
    """
    Returns real-time CPU and RAM usage percentage.
    """
    if is_windows():
        cmd = 'Get-CimInstance Win32_Processor | Select-Object -ExpandProperty LoadPercentage; ' \
              '(Get-CimInstance Win32_OperatingSystem | Select-Object @{N=\'Usage\';E={100 - ($_.FreePhysicalMemory / $_.TotalVisibleMemorySize) * 100}}).Usage'
    else:
        cmd = "top -bn1 | grep 'Cpu(s)' | sed 's/.*, *\([0-9.]*\)%* id.*/\1/' | awk '{print 100 - $1}'; " \
              "free | grep Mem | awk '{print $3/$2 * 100.0}'"

    success, output = run_command(cmd)
    if success:
        lines = output.strip().split('\n')
        if len(lines) >= 2:
            cpu = lines[0].strip()
            ram = lines[1].strip()
            return f"CPU Usage: {cpu}% | RAM Usage: {float(ram):.1f}%"
    return "Error fetching resources"
