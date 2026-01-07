# Cross-Platform OS Utility Tool

A comprehensive system utility application built with Python and Tkinter that runs on both **Windows 10+** and **Ubuntu 20.04+**.

## 🚀 Features
- **File Cleanup**: Clean temp files, logs, and caches.
- **Disk Analysis**: Monitor space and list root directory contents.
- **Process Management**: View active processes and terminate them by PID.
- **System Information**: Real-time CPU/RAM monitoring and hardware info.
- **Networking**: IP addresses and interface status.
- **Security**: Windows Defender and ClamAV integration.
- **Startup Manager**: View applications scheduled to run at boot.

## 🛠 Technology Stack
- **Language**: Python 3.x
- **GUI**: Tkinter (ttk)
- **Engine**: `subprocess` module for system calls.
- **Detection**: `platform` module for runtime OS identification.

## 🏗 OS Abstraction Logic
The project achieves OS abstraction by using a modular command execution patterns:
1. **OS Detection**: `os_detector.py` identifies the platform at startup.
2. **Command Abstraction**: `command_runner.py` detects the platform and determines whether to wrapper commands in PowerShell (Windows) or execute directly in shell (Linux/Bash).
3. **Action Modules**: Each module in `actions/` contains logic for both Windows and Linux commands, ensuring the same GUI button works seamlessly regardless of the environment.

## 📝 Operating System Concepts Demonstrated
- **Process Management**: Handling process lifecycles, PID-based termination, and resource prioritization.
- **System Calls**: Interacting with the kernel via shell commands and CimInstances.
- **File System Operations**: Recursive deletion, permission handling, and directory traversal.
- **Security Integration**: Interfacing with system-level security providers (Defender/ClamAV).
- **Resource Monitoring**: Real-time data acquisition from system performance counters.

## 🏃 Running the Application
```bash
python -m os_utility_tool.main
```
*Note: Running as Administrator (Windows) or Sudo (Linux) is recommended for full functionality.*
