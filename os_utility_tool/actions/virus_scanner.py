import subprocess
import os
import shutil
import ctypes
import datetime
import hashlib
import threading
from os_utility_tool.os_detector import is_windows, is_linux
from os_utility_tool.utils.command_runner import run_command

SCAN_LOG = "scan_report.txt"

def is_admin():
    """Checks if the current process has administrative/root privileges."""
    try:
        if is_windows():
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            return os.getuid() == 0
    except Exception:
        return False

class NativePythonScanner:
    """
    An open-source, built-in scanner that works even if 
    system tools (like Defender) are disabled.
    """
    def __init__(self, log_file):
        self.log_file = log_file
        self.suspicious_extensions = ['.exe', '.bat', '.ps1', '.vbs', '.js', '.scr', '.vbe']
        self.dangerous_keywords = ['malware', 'hack', 'crack', 'keygen', 'payload']
        
    def scan(self, path):
        with open(self.log_file, 'a') as f:
            f.write(f"\n[ENGINE: NATIVE PYTHON GUARD]\n")
            f.write(f"Status: Scanning directory: {path}\n")
            f.write("-" * 40 + "\n")
            
            scanned_count = 0
            threat_count = 0
            
            for root, dirs, files in os.walk(path):
                # Optimization: skip large/hidden system folders
                if any(x in root.lower() for x in ['.git', '__pycache__', 'node_modules', '.venv']):
                    continue
                    
                for file in files:
                    scanned_count += 1
                    file_path = os.path.join(root, file)
                    threats = self.check_file(file_path, file)
                    if threats:
                        threat_count += len(threats)
                        f.write(f"[DETECTED] {file_path}\n")
                        for t in threats:
                            f.write(f"   -> Reason: {t}\n")
            
            f.write("-" * 40 + "\n")
            f.write(f"Scan Finished.\n")
            f.write(f"Total Files Scanned: {scanned_count}\n")
            f.write(f"Threats Detected: {threat_count}\n")
            if threat_count == 0:
                f.write("Verdict: System appears CLEAN (Native Guard).\n")

    def check_file(self, full_path, filename):
        reasons = []
        name_lower = filename.lower()
        
        # 1. Double Extension Check (e.g., photo.jpg.exe)
        parts = filename.split('.')
        if len(parts) > 2:
            ext = f".{parts[-1]}"
            if ext in self.suspicious_extensions:
                reasons.append("Suspicious double extension (potential masquerading)")

        # 2. Hidden Executable Check
        if filename.startswith('.') and any(name_lower.endswith(ext) for ext in self.suspicious_extensions):
            reasons.append("Hidden executable file")

        # 3. Known Malware Keywords
        if any(kw in name_lower for kw in self.dangerous_keywords):
            reasons.append("File name matches known malicious patterns")
            
        return reasons

def run_malware_scan(target_path=None, scan_type=1):
    """
    Starts a malware scan.
    target_path: Path to scan (if None, scans project dir or uses Defender default)
    scan_type: 1 (Quick), 2 (Full/C:), 3 (Custom Folder)
    """
    if os.path.exists(SCAN_LOG):
        try: os.remove(SCAN_LOG)
        except: pass

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = f"Scan initiated at: {current_time}\n"
    header += f"User Status: {'Administrator' if is_admin() else 'Standard User'}\n"
    
    # Resolve target path
    if target_path is None:
        if scan_type == 2 and is_windows():
            target_path = "C:\\"
        else:
            target_path = os.getcwd()

    header += f"Target Path: {target_path}\n"
    header += "-" * 40 + "\n"
    
    # Check if Defender service is alive on Windows
    defender_broken = False
    if is_windows():
        success, svc_info = run_command("Get-Service WinDefend | Select-Object -ExpandProperty Status")
        if not success or "Running" not in svc_info:
            defender_broken = True

    if is_windows() and not defender_broken:
        # Try primary engine (Defender)
        potential_paths = [
            r"C:\Program Files\Windows Defender\MpCmdRun.exe",
            r"C:\ProgramData\Microsoft\Windows Defender\Platform"
        ]
        defender_path = None
        for path in potential_paths:
            if os.path.isfile(path): defender_path = path; break
            elif os.path.isdir(path):
                for root, dirs, files in os.walk(path):
                    if "MpCmdRun.exe" in files:
                        defender_path = os.path.join(root, "MpCmdRun.exe")
                        break
            if defender_path: break

        if defender_path:
            with open(SCAN_LOG, 'w') as f: f.write(header + "Primary Engine: Windows Defender\n")
            
            # Build Defender command
            if scan_type == 3: # Custom
                cmd = f'"{defender_path}" -Scan -ScanType 3 -File "{target_path}" >> {SCAN_LOG} 2>&1'
            else:
                cmd = f'"{defender_path}" -Scan -ScanType {scan_type} >> {SCAN_LOG} 2>&1'
                
            subprocess.Popen(cmd, shell=True)
            return f"SUCCESS: Windows Defender scan ({'Quick' if scan_type==1 else 'Full' if scan_type==2 else 'Custom'}) started."

    # FALLBACK: Native Python Scanner
    with open(SCAN_LOG, 'w') as f: 
        f.write(header + "Primary Engine: PYTHON NATIVE GUARD (Open Source Fallback)\n")
        f.write("Reason: System services unavailable or manual override.\n")
    
    scanner = NativePythonScanner(SCAN_LOG)
    scan_thread = threading.Thread(target=scanner.scan, args=(target_path,))
    scan_thread.daemon = True
    scan_thread.start()
    
    return f"SUCCESS: Native Guard Scan started on {target_path}."

def get_scan_results():
    """
    Checks for running scans or returns interpreted content of the log file.
    """
    # Check for running processes
    if is_linux():
        success, output = run_command("pgrep clamscan")
        if success and output.strip(): return f"STATUS: ClamAV is RUNNING..."
    else:
        success, output = run_command("tasklist /FI \"IMAGENAME eq MpCmdRun.exe\"")
        if success and "MpCmdRun.exe" in output: return f"STATUS: Windows Defender is RUNNING..."

    if os.path.exists(SCAN_LOG):
        try:
            with open(SCAN_LOG, 'r') as f:
                content = f.read()
                if not content.strip(): return "STATUS: Initializing scan..."
                
                # Check for the Defender error we keeps hitting
                if "0x80004005" in content and "NATIVE PYTHON GUARD" not in content:
                    # Automatically trigger fallback if we see the error
                    run_malware_scan()
                    return "STATUS: Windows Defender failed (Access Denied). Switching to Native Guard..."

                return f"RESULTS:\n\n{content[-2000:]}"
        except Exception as e:
            return f"Error reading log: {str(e)}"
    
    return "STATUS: No report found. Click 'Malware Scan' to start."

