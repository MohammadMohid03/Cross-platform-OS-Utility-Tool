import os
import sys

# Add the project root to sys.path
sys.path.append(os.getcwd())

from os_utility_tool.actions.virus_scanner import run_malware_scan, get_scan_results
import time

print("Starting scan...")
res = run_malware_scan()
print(res)

if "SUCCESS" in res:
    print("Waiting a few seconds for scan to start/log...")
    time.sleep(5)
    print("Checking results...")
    results = get_scan_results()
    print(results)
else:
    print("Scan failed to start.")
