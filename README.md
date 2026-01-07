# Cross-Platform OS Utility Tool

A cross-platform desktop system utility built with Python + Tkinter. It provides a single GUI for common OS tasks (cleanup, system info, process management, disk/network info, startup apps) and includes a simple malware scan workflow with Windows Defender support (Windows) plus a built-in fallback scanner.

## Features

- System cleanup
  - Temp cleanup
  - Cache cleanup
- Disk tools
  - Disk usage summary
  - Root directory listing
- Process management
  - List running processes
  - Kill a process by PID
- System information
  - Hardware / OS information
  - Live CPU/RAM monitor in the sidebar
- Network information
  - Basic network configuration details
- Startup applications
  - View startup entries (platform-dependent)
- Malware scan
  - Uses Windows Defender when available (Windows)
  - Falls back to a native Python “Guard” scanner when system tools aren’t available
  - Writes results to `scan_report.txt`

## Supported platforms

- Windows 10/11
- Ubuntu 20.04+ (or similar Linux distros)

Some actions require Administrator (Windows) / root (Linux) privileges.

## Requirements

- Python 3.10+ recommended (3.8+ likely works)
- Tkinter
  - Windows/macOS: usually included with Python
  - Ubuntu/Debian: you may need `python3-tk`

No third‑party Python packages are required for the core app.

## Installation

Clone the repo:

```bash
git clone https://github.com/MohammadMohid03/Cross-platform-OS-Utility-Tool.git
cd Cross-platform-OS-Utility-Tool
```

(Optional but recommended) create and activate a virtual environment:

```bash
python -m venv .venv
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
# Linux/macOS
source .venv/bin/activate
```

## Run

Start the GUI:

```bash
python -m os_utility_tool.main
```

If you see warnings about privileges, re-run:

- Windows: open PowerShell as Administrator
- Linux: run with `sudo` if needed

## Malware scan output

- Scan results are written to `scan_report.txt` in the current working directory.
- The GUI includes a “View Logs” action to display recent scan output.

## Project structure

- `os_utility_tool/main.py` — application entry point (Tkinter root + app startup)
- `os_utility_tool/gui.py` — GUI layout and button wiring
- `os_utility_tool/actions/` — platform-aware utility actions (cleanup, disk, processes, etc.)
- `os_utility_tool/utils/command_runner.py` — command execution helper
- `os_utility_tool/os_detector.py` — OS detection helpers
- `test_virus_scan.py` — simple test script for scanning behavior

## Notes / limitations

- Some features depend on OS tools and permissions; behavior varies by platform.
- On Linux, certain actions may require additional system utilities to be installed.

## Contributing

Issues and pull requests are welcome:

1. Fork the repository
2. Create a feature branch
3. Open a PR with a clear description and screenshots (if UI-related)

## License

Add a license if you plan to distribute this publicly (MIT is a common choice).