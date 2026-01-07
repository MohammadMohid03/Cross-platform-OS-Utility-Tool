from os_utility_tool.os_detector import is_windows
from os_utility_tool.utils.command_runner import run_command

def get_network_info():
    """
    Displays IP address, network interfaces, and connection status.
    Demonstrates: Network management.
    """
    if is_windows():
        cmd = 'Get-NetIPAddress -AddressFamily IPv4 | Select-Object InterfaceAlias, IPAddress, PrefixLength | Out-String; ' \
              'Get-NetAdapter | Select-Object Name, Status, LinkSpeed | Out-String'
    else:
        cmd = 'echo "--- IP Addresses ---"; ip -4 -br addr; echo "\n--- Interface Status ---"; ip link'

    success, output = run_command(cmd)
    return output if success else f"Error: {output}"
