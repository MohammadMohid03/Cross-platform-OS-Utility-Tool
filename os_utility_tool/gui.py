import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
import datetime

# Import actions
from os_utility_tool.actions import (
    temp_cleaner, disk_analyzer, process_manager, 
    system_info, network_info, startup_manager,
    virus_scanner, cache_cleaner, resource_monitor, 
    home_analyzer
)
from os_utility_tool.os_detector import get_os

# Modern Color Palette
COLORS = {
    "bg_dark": "#0f172a",      # Slate 900
    "bg_sidebar": "#1e293b",   # Slate 800
    "accent": "#10b981",       # Emerald 500
    "accent_hover": "#059669", # Emerald 600
    "text_primary": "#f8fafc", # Slate 50
    "text_secondary": "#94a3b8", # Slate 400
    "card_bg": "#334155",      # Slate 700
    "error": "#ef4444",        # Red 500
    "warning": "#f59e0b"       # Amber 500
}

class OSUtilityApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"OmniOS Utility Pro - {get_os()}")
        self.root.geometry("1100x750")
        self.root.configure(bg=COLORS["bg_dark"])
        
        # Performance state
        self.cpu_val = 0
        self.ram_val = 0
        self.is_running_task = False

        self.setup_styles()
        self.create_layout()
        self.start_monitoring()
        self.animate_intro()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Global Frame Style
        style.configure("TFrame", background=COLORS["bg_dark"])
        style.configure("Sidebar.TFrame", background=COLORS["bg_sidebar"])
        
        # Sidebar Button Style
        style.configure("Sidebar.TButton", 
                        padding=12, 
                        font=('Segoe UI', 10, 'bold'), 
                        background=COLORS["bg_sidebar"], 
                        foreground=COLORS["text_primary"],
                        borderwidth=0)
        style.map("Sidebar.TButton", 
                  background=[('active', COLORS["accent"]), ('pressed', COLORS["accent_hover"])],
                  foreground=[('active', 'white')])

        # Action Button Style
        style.configure("Action.TButton", 
                        padding=10, 
                        font=('Segoe UI', 10), 
                        background=COLORS["accent"], 
                        foreground="white")
        style.map("Action.TButton", background=[('active', COLORS["accent_hover"])])
        
        # Labels
        style.configure("Header.TLabel", 
                        font=('Segoe UI', 18, 'bold'), 
                        background=COLORS["bg_dark"], 
                        foreground=COLORS["text_primary"])
        
        style.configure("Stat.TLabel", 
                        font=('Segoe UI', 11, 'bold'), 
                        background=COLORS["bg_sidebar"], 
                        foreground=COLORS["accent"])

        style.configure("Sub.TLabel", 
                        font=('Segoe UI', 9), 
                        background=COLORS["bg_sidebar"], 
                        foreground=COLORS["text_secondary"])

    def create_layout(self):
        # Sidebar
        self.sidebar = ttk.Frame(self.root, style="Sidebar.TFrame", width=260)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        # App Logo/Title in Sidebar
        logo_label = tk.Label(self.sidebar, text="🚀 OMNIOS PRO", 
                             font=('Segoe UI', 16, 'bold'), 
                             bg=COLORS["bg_sidebar"], fg=COLORS["accent"])
        logo_label.pack(pady=30)

        # Navigation Buttons
        nav_items = [
            ("🏠 Dashboard", self.show_dashboard),
            ("🧹 System Clean", self.run_temp_clean),
            ("📊 Process Manager", self.run_process_list),
            ("🏠 Home Analyzer", self.run_home_analyzer),
            ("💾 Disk Analysis", self.run_disk_analyzer),
            ("🔄 Cache Flush", self.run_cache_clean),
            ("⚡ Startup Apps", self.run_startup_list),
            ("🌐 Network Info", self.run_net_info),
            ("🛡️ Malware Scan", self.run_virus_scan),
            ("📝 View Logs", self.view_scan_log),
            ("⚙️ System Stats", self.run_sys_info),
            ("📁 Root Files", self.run_list_files),
        ]

        for text, cmd in nav_items:
            btn = ttk.Button(self.sidebar, text=text, command=cmd, style="Sidebar.TButton")
            btn.pack(fill=tk.X, padx=10, pady=2)

        # Sidebar Footer (Monitors)
        footer = ttk.Frame(self.sidebar, style="Sidebar.TFrame")
        footer.pack(side=tk.BOTTOM, fill=tk.X, pady=20, padx=20)
        
        self.cpu_label = ttk.Label(footer, text="CPU: 0%", style="Stat.TLabel")
        self.cpu_label.pack(anchor=tk.W)
        self.cpu_sub = ttk.Label(footer, text="Processing Load", style="Sub.TLabel")
        self.cpu_sub.pack(anchor=tk.W, pady=(0, 10))

        self.ram_label = ttk.Label(footer, text="RAM: 0%", style="Stat.TLabel")
        self.ram_label.pack(anchor=tk.W)
        self.ram_sub = ttk.Label(footer, text="Memory Usage", style="Sub.TLabel")
        self.ram_sub.pack(anchor=tk.W)

        # Main Content Area
        self.content_area = ttk.Frame(self.root)
        self.content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=30, pady=30)

        # Header Section
        self.header_frame = ttk.Frame(self.content_area)
        self.header_frame.pack(fill=tk.X)
        
        self.title_label = ttk.Label(self.header_frame, text="System Dashboard", style="Header.TLabel")
        self.title_label.pack(side=tk.LEFT)
        
        self.status_indicator = tk.Label(self.header_frame, text="● SYSTEM READY", 
                                        font=('Segoe UI', 9, 'bold'), 
                                        bg=COLORS["bg_dark"], fg=COLORS["accent"])
        self.status_indicator.pack(side=tk.RIGHT)

        # Separator line
        sep = tk.Frame(self.content_area, height=1, bg=COLORS["card_bg"])
        sep.pack(fill=tk.X, pady=15)

        # Task/Output Section
        self.output_container = ttk.Frame(self.content_area)
        self.output_container.pack(fill=tk.BOTH, expand=True)

        self.output_area = scrolledtext.ScrolledText(
            self.output_container, 
            bg=COLORS["bg_sidebar"], 
            fg=COLORS["text_primary"], 
            insertbackground="white",
            font=('Consolas', 11),
            padx=15, pady=15,
            borderwidth=0,
            highlightthickness=0
        )
        self.output_area.pack(fill=tk.BOTH, expand=True)

        # Action Bar (Bottom Tools)
        self.action_bar = ttk.Frame(self.content_area)
        self.action_bar.pack(fill=tk.X, pady=(20, 0))

        ttk.Label(self.action_bar, text="Quick Kill PID:", 
                  font=('Segoe UI', 9), background=COLORS["bg_dark"], 
                  foreground=COLORS["text_secondary"]).pack(side=tk.LEFT)
        
        self.pid_entry = tk.Entry(self.action_bar, bg=COLORS["bg_sidebar"], 
                                 fg="white", borderwidth=0, font=('Segoe UI', 10),
                                 highlightbackground=COLORS["card_bg"], highlightthickness=1, width=15)
        self.pid_entry.pack(side=tk.LEFT, padx=10, ipady=3)
        
        ttk.Button(self.action_bar, text="Terminte Process", 
                   command=self.run_kill_process, style="Action.TButton").pack(side=tk.LEFT)

        ttk.Button(self.action_bar, text="Refresh Dashboard", 
                   command=self.show_dashboard, style="Action.TButton").pack(side=tk.RIGHT)

    def log(self, message):
        self.output_area.delete('1.0', tk.END)
        # Add typing effect or just smooth insert
        self.output_area.insert(tk.END, message)
        self.set_ready()

    def set_busy(self, text):
        self.is_running_task = True
        self.status_indicator.config(text=f"● EXECUTING: {text.upper()}", fg=COLORS["warning"])
        self.root.update_idletasks()

    def set_ready(self):
        self.is_running_task = False
        self.status_indicator.config(text="● SYSTEM READY", fg=COLORS["accent"])

    def show_dashboard(self):
        self.title_label.config(text="System Dashboard")
        self.set_busy("Scanning System")
        dash_content = f"--- OMNIOS PRO SYSTEM HEALTH ---\n"
        dash_content += f"Report Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        dash_content += f"Platform: {get_os()}\n"
        dash_content += f"Elevated Privileges: {'YES' if self.is_admin() else 'NO'}\n"
        dash_content += "-" * 40 + "\n\n"
        
        # Pull process info as a summary
        dash_content += "Top 5 Resource Consumers:\n"
        res = process_manager.list_processes()
        # Extract first 6 lines of process list
        dash_content += "\n".join(res.split('\n')[:7])
        
        self.log(dash_content)

    def is_admin(self):
        import ctypes, os
        try:
            if get_os() == "Windows": return ctypes.windll.shell32.IsUserAnAdmin() != 0
            else: return os.getuid() == 0
        except: return False

    # Action Wrappers
    def run_temp_clean(self):
        self.title_label.config(text="Temp Files Cleanup")
        self.set_busy("Cleaning Temp")
        self.log(temp_cleaner.clean_temp_files())

    def run_disk_analyzer(self):
        self.title_label.config(text="Disk Usage Analysis")
        self.set_busy("Analyzing Disk")
        self.log(disk_analyzer.get_disk_usage())

    def run_list_files(self):
        self.title_label.config(text="Root Directory Contents")
        self.set_busy("Listing Files")
        self.log(disk_analyzer.list_root_files())

    def run_sys_info(self):
        self.title_label.config(text="Hardware Information")
        self.set_busy("Gathering Info")
        self.log(system_info.get_system_info())

    def run_net_info(self):
        self.title_label.config(text="Network Configuration")
        self.set_busy("Fetching Network")
        self.log(network_info.get_network_info())

    def run_startup_list(self):
        self.title_label.config(text="Startup Applications")
        self.set_busy("Reading Reg/Autostart")
        self.log(startup_manager.list_startup_programs())

    def run_process_list(self):
        self.title_label.config(text="Active Process Monitor")
        self.set_busy("Listing Processes")
        self.log(process_manager.list_processes())

    def run_home_analyzer(self):
        self.title_label.config(text="Home Directory Analytics")
        self.set_busy("Calculating Sizes")
        self.log(home_analyzer.analyze_home_directory())

    def run_virus_scan(self):
        from tkinter import filedialog
        self.title_label.config(text="Malware Security Scan")
        
        choice = messagebox.askquestion("Security Hub", 
                                      "Select scan scope:\n\n"
                                      "Yes: Custom Folder Scan\n"
                                      "No: System Quick Scan\n"
                                      "Cancel: Abort", 
                                      icon='info', type='yesnocancel')
        
        if choice == 'yes':
            folder = filedialog.askdirectory()
            if folder:
                self.set_busy("Scanning Folder")
                self.log(virus_scanner.run_malware_scan(target_path=folder, scan_type=3))
        elif choice == 'no':
            self.set_busy("Quick Scan")
            self.log(virus_scanner.run_malware_scan(scan_type=1))

    def run_full_scan(self):
        self.title_label.config(text="Full Security Audit")
        if messagebox.askyesno("Confirm Audit", "Run deep-scan on C: Disk? (Heavy CPU usage)"):
            self.set_busy("Full Scan")
            self.log(virus_scanner.run_malware_scan(scan_type=2))

    def view_scan_log(self):
        self.title_label.config(text="Security Logs")
        self.log(virus_scanner.get_scan_results())

    def run_cache_clean(self):
        self.title_label.config(text="Cache & Log Flushing")
        self.set_busy("Flushing Cache")
        self.log(cache_cleaner.clean_cache_and_logs())

    def run_kill_process(self):
        pid = self.pid_entry.get()
        if not pid: return
        if messagebox.askyesno("Process Guard", f"Force terminate PID {pid}?"):
            self.set_busy("Killing PID")
            self.log(process_manager.kill_process(pid))

    def start_monitoring(self):
        def monitor_loop():
            while True:
                try:
                    res = resource_monitor.get_live_resources()
                    # Parse "CPU Usage: 5% | RAM Usage: 45.2%"
                    cpu_part = res.split('|')[0].replace("CPU Usage:", "").replace("%", "").strip()
                    ram_part = res.split('|')[1].replace("RAM Usage:", "").replace("%", "").strip()
                    
                    self.cpu_val = float(cpu_part)
                    self.ram_val = float(ram_part)
                    
                    self.update_monitors()
                except: pass
                time.sleep(2)
        
        thread = threading.Thread(target=monitor_loop, daemon=True)
        thread.start()

    def update_monitors(self):
        # Update colors based on load
        cpu_color = COLORS["accent"] if self.cpu_val < 70 else COLORS["warning"] if self.cpu_val < 90 else COLORS["error"]
        ram_color = COLORS["accent"] if self.ram_val < 70 else COLORS["warning"] if self.ram_val < 90 else COLORS["error"]
        
        self.cpu_label.config(text=f"CPU: {self.cpu_val}%", foreground=cpu_color)
        self.ram_label.config(text=f"RAM: {self.ram_val}%", foreground=ram_color)

    def animate_intro(self):
        # Initial fade in text effect
        original_text = self.output_area.get('1.0', tk.END)
        self.output_area.delete('1.0', tk.END)
        welcome = f"🚀 OMNIOS PRO VERSION 2.0 INFUSED WITH AGENTIC AI\n"
        welcome += f"System: {get_os()} | Kernel: Active\n"
        welcome += "="*45 + "\n"
        welcome += "Welcome! All modules loaded successfully.\n"
        welcome += f"Initialization complete at {datetime.datetime.now().strftime('%H:%M:%S')}\n"
        
        def type_text(txt, i=0):
            if i < len(txt):
                self.output_area.insert(tk.END, txt[i])
                self.root.after(10, lambda: type_text(txt, i+1))
        
        type_text(welcome)

if __name__ == "__main__":
    root = tk.Tk()
    # Simple window drag animation/transparency if supported
    try: root.attributes('-alpha', 0.98)
    except: pass
    app = OSUtilityApp(root)
    root.mainloop()

