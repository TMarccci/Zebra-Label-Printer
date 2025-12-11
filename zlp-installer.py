import tkinter as tk
from tkinter import ttk, messagebox
import os
import subprocess
import json
from pathlib import Path
try:
    import win32com.client as win32
except Exception:
    win32 = None
import urllib.request
import sys

def resource_path(relative_path):
    try:
        base = sys._MEIPASS
        print(f"Base path (frozen): {base}")
    except:
        base = os.path.abspath(".")
        print(f"Base path: {base}")
    return os.path.join(base, relative_path)

class ZebraLabelPrinterInstaller:
    def __init__(self, root):
        self.root = root
        self.root.title("Zebra Label Printer Installer")
        self.root.geometry("640x420")
        self.username = os.getenv("USERNAME")
        self.install_path = f"C:\\Users\\{self.username}\\Zebra Label Printer"
        self.create_desktop_icon = tk.BooleanVar(value=True)
        self.start_with_windows = tk.BooleanVar(value=True)
        self.launch_app = tk.BooleanVar(value=True)
        self.progress = None
        self.log_text = None
        self.next_button = None
        
        self.show_welcome_page()
    
    def show_welcome_page(self):
        self.clear_window()
        ttk.Label(self.root, text="Welcome", font=("Arial", 16, "bold")).pack(pady=12)
        ttk.Label(
            self.root,
            text=(
                "Welcome to the Zebra Label Printer Installer.\n"
                "This wizard will guide you through setup."
            ),
            justify="center",
        ).pack(pady=8)

        ttk.Separator(self.root, orient="horizontal").pack(fill="x", pady=12)

        footer = ttk.Frame(self.root)
        footer.pack(side="bottom", fill="x", padx=12, pady=12)
        ttk.Button(footer, text="Next", command=self.show_options_page).pack(side="right")
    
    def show_options_page(self):
        self.clear_window()
        ttk.Label(self.root, text="Setup Options", font=("Arial", 16, "bold")).pack(pady=12)

        body = ttk.Frame(self.root)
        body.pack(fill="both", expand=True, padx=40, pady=10)
        ttk.Checkbutton(body, text="Create Desktop Icon", variable=self.create_desktop_icon).pack(anchor="w", pady=6)
        ttk.Checkbutton(body, text="Start with Windows", variable=self.start_with_windows).pack(anchor="w", pady=6)

        ttk.Separator(self.root, orient="horizontal").pack(fill="x", pady=12)

        footer = ttk.Frame(self.root)
        footer.pack(side="bottom", fill="x", padx=12, pady=12)
        ttk.Button(footer, text="Back", command=self.show_welcome_page).pack(side="left")
        ttk.Button(footer, text="Next", command=self.show_log_page_and_download).pack(side="right")
    
    def show_log_page_and_download(self):
        self.clear_window()
        ttk.Label(self.root, text="Downloading and Configuring", font=("Arial", 16, "bold")).pack(pady=12)

        container = ttk.Frame(self.root)
        container.pack(fill="both", expand=True, padx=12, pady=8)

        # Log output
        text_frame = ttk.Frame(container)
        text_frame.pack(fill="both", expand=True)
        self.log_text = tk.Text(text_frame, height=12, wrap="word")
        y_scroll = ttk.Scrollbar(text_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=y_scroll.set)
        self.log_text.pack(side="left", fill="both", expand=True)
        y_scroll.pack(side="right", fill="y")

        # Progress bar
        self.progress = ttk.Progressbar(self.root, length=520, mode="indeterminate")
        self.progress.pack(pady=8)
        self.progress.start()

        ttk.Separator(self.root, orient="horizontal").pack(fill="x", pady=8)

        footer = ttk.Frame(self.root)
        footer.pack(side="bottom", fill="x", padx=12, pady=12)
        self.next_button = ttk.Button(footer, text="Next", state="disabled", command=self.show_completion_page)
        self.next_button.pack(side="right")
        ttk.Button(footer, text="Back", command=self.show_options_page).pack(side="left")

        # Start the actual work shortly so UI renders first
        self.root.after(100, self.perform_download_and_setup)
    
    def perform_download_and_setup(self):
        success = True
        try:
            self._log(f"Creating install directory: {self.install_path}")
            os.makedirs(self.install_path, exist_ok=True)

            files = ["Zebra-Label-Printer.exe", "zlp-server.exe", "zlp-updater.exe"]
            api_url = "https://api.github.com/repos/TMarccci/Zebra-Label-Printer/releases/latest"

            self._log("Fetching latest release info from GitHub...")
            with urllib.request.urlopen(api_url) as response:
                release_data = json.loads(response.read())

            for file in files:
                asset = next((a for a in release_data.get("assets", []) if a.get("name") == file), None)
                if asset:
                    file_path = os.path.join(self.install_path, file)
                    self._log(f"Downloading {file}...")
                    urllib.request.urlretrieve(asset["browser_download_url"], file_path)
                    self._log(f"Downloaded {file} -> {file_path}")
                else:
                    self._log(f"Warning: Asset not found for {file}")

            if self.create_desktop_icon.get():
                try:
                    self._log("Creating desktop icon...")
                    self.create_shortcut()
                    self._log("Desktop icon created.")
                except Exception as e:
                    self._log(f"Error creating desktop icon: {e}")

            if self.start_with_windows.get():
                try:
                    self._log("Adding app to Windows Startup...")
                    self.add_to_startup()
                    self._log("Added to Startup.")
                except Exception as e:
                    self._log(f"Error adding to Startup: {e}")

            self._log("All tasks completed.")
        except Exception as e:
            success = False
            messagebox.showerror("Error", f"Download/setup failed: {str(e)}")
            self._log(f"Setup failed: {e}")
        finally:
            if self.progress:
                self.progress.stop()
            if self.next_button:
                self.next_button.config(state="normal")
            if success:
                # Auto-advance to completion page when done
                self.root.after(300, self.show_completion_page)
    
    def show_completion_page(self):
        self.clear_window()
        ttk.Label(self.root, text="Installation Complete", font=("Arial", 16, "bold")).pack(pady=12)

        body = ttk.Frame(self.root)
        body.pack(fill="both", expand=True, padx=40, pady=10)
        ttk.Checkbutton(body, text="Start the app now", variable=self.launch_app).pack(anchor="w", pady=6)

        ttk.Separator(self.root, orient="horizontal").pack(fill="x", pady=12)

        footer = ttk.Frame(self.root)
        footer.pack(side="bottom", fill="x", padx=12, pady=12)
        ttk.Button(footer, text="Finish", command=self.finish_installation).pack(side="right")

    def finish_installation(self):
        if self.launch_app.get():
            try:
                subprocess.Popen(os.path.join(self.install_path, "Zebra-Label-Printer.exe"))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to launch app: {e}")
        self.root.quit()

    def create_shortcut(self):
        desktop = Path.home() / "Desktop"
        shortcut_path = desktop / "Zebra Label Printer.lnk"
        target = os.path.join(self.install_path, "Zebra-Label-Printer.exe")

        if win32 is None:
            raise RuntimeError("pywin32 not available to create shortcut")

        shell = win32.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(str(shortcut_path))
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = os.path.dirname(target)
        shortcut.IconLocation = target
        shortcut.Description = "Zebra Label Printer"
        shortcut.save()
        
    def add_to_startup(self):
        startup_folder = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
        shortcut_path = startup_folder / "Zebra Label Printer.lnk"
        target = os.path.join(self.install_path, "Zebra-Label-Printer.exe")

        if win32 is None:
            raise RuntimeError("pywin32 not available to create startup shortcut")

        shell = win32.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(str(shortcut_path))
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = os.path.dirname(target)
        shortcut.IconLocation = target
        shortcut.Description = "Zebra Label Printer"
        shortcut.save()
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def _log(self, message: str):
        if self.log_text is not None:
            self.log_text.insert("end", message + "\n")
            self.log_text.see("end")
            self.root.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap(resource_path("static/icon.ico"))
    app = ZebraLabelPrinterInstaller(root)
    root.mainloop()