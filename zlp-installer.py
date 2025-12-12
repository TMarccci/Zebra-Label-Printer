import tkinter as tk
from tkinter import ttk, messagebox
import os
import subprocess
import json
from pathlib import Path
import threading
import requests
import win32com.client as win32
import pythoncom
import urllib.request

from zlp_lib.zlp import resource_path, APP_FOLDER, CURRENT_PROGRAM_VERSION, USER

class ZebraLabelPrinterInstaller:
    def __init__(self, root):
        self.root = root
        self.root.title("Zebra Label Printer Installer")
        self.root.geometry("640x420")
        self.username = USER
        self.install_path = APP_FOLDER
        self.create_desktop_icon = tk.BooleanVar(value=True)
        self.start_with_windows = tk.BooleanVar(value=True)
        self.launch_app = tk.BooleanVar(value=True)
        self.progress = None
        self.log_text = None
        self.next_button = None
        self.progress_label = None
        self._dot_ticks = 0
        self._downloading = False
        
        self.show_welcome_page()
    
    def show_welcome_page(self):
        self.clear_window()
        ttk.Label(self.root, text="Welcome", font=("Arial", 16, "bold")).pack(pady=12)
        ttk.Label(
            self.root,
            text=(
                f"Welcome to the Zebra Label Printer Installer.\n"
                f"Installation version: {CURRENT_PROGRAM_VERSION}\n\n\n"
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

        # Progress indicator (percentage + animated dots)
        self.progress_label = ttk.Label(self.root, text="Preparing downloads...")
        self.progress_label.pack(pady=(0,4))
        self.progress = ttk.Progressbar(self.root, length=520, mode="determinate", maximum=100)
        self.progress.pack(pady=4)
        self.progress['value'] = 0

        ttk.Separator(self.root, orient="horizontal").pack(fill="x", pady=8)

        footer = ttk.Frame(self.root)
        footer.pack(side="bottom", fill="x", padx=12, pady=12)
        self.next_button = ttk.Button(footer, text="Next", state="disabled", command=self.show_completion_page)
        self.next_button.pack(side="right")
        ttk.Button(footer, text="Back", command=self.show_options_page).pack(side="left")

        # Start the actual work in background so UI stays responsive
        threading.Thread(target=self.perform_download_and_setup_thread, daemon=True).start()
        # Start dots animation
        self._downloading = True
        self.root.after(300, self._animate_dots)
    
    def _animate_dots(self):
        if not self._downloading or self.progress_label is None:
            return
        self._dot_ticks = (self._dot_ticks + 1) % 4
        dots = "." * self._dot_ticks
        # keep existing text prefix, replace trailing dots
        text = self.progress_label.cget("text")
        base = text.split(".")[0]
        self.progress_label.config(text=f"{base}{dots}")
        self.root.after(600, self._animate_dots)

    def perform_download_and_setup_thread(self):
        success = True
        try:
            self._log(f"Creating install directory: {self.install_path}")
            os.makedirs(self.install_path, exist_ok=True)

            files = ["Zebra-Label-Printer.exe", "zlp-server.exe", "zlp-updater.exe", "zlp-uninstaller.exe"]
            api_url = "https://api.github.com/repos/TMarccci/Zebra-Label-Printer/releases/latest"

            self._log("Fetching latest release info from GitHub...")
            with urllib.request.urlopen(api_url) as response:
                release_data = json.loads(response.read())

            for file in files:
                asset = next((a for a in release_data.get("assets", []) if a.get("name") == file), None)
                if asset:
                    url = asset["browser_download_url"]
                    file_path = os.path.join(self.install_path, file)
                    self._log(f"Downloading {file}...")
                    # Update label and reset progress
                    self._set_progress_label(f"Downloading {file}")
                    self._set_progress_value(0)
                    try:
                        self._stream_download(url, file_path)
                        self._log(f"Downloaded {file} -> {file_path}")
                    except Exception as e:
                        self._log(f"Error downloading {file}: {e}")
                        raise
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
            # done animating
            self._downloading = False
            if self.progress:
                self._set_progress_value(100)
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
        # Ensure COM is initialized for this background thread
        if pythoncom is not None:
            pythoncom.CoInitialize()
        try:
            shell = win32.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortcut(str(shortcut_path))
            shortcut.Targetpath = target
            shortcut.WorkingDirectory = os.path.dirname(target)
            shortcut.IconLocation = target
            shortcut.Description = "Zebra Label Printer"
            shortcut.save()
        finally:
            if pythoncom is not None:
                pythoncom.CoUninitialize()
        
    def add_to_startup(self):
        startup_folder = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
        shortcut_path = startup_folder / "Zebra Label Printer.lnk"
        target = os.path.join(self.install_path, "Zebra-Label-Printer.exe")

        if win32 is None:
            raise RuntimeError("pywin32 not available to create startup shortcut")
        # Ensure COM is initialized for this background thread
        if pythoncom is not None:
            pythoncom.CoInitialize()
        try:
            shell = win32.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortcut(str(shortcut_path))
            shortcut.Targetpath = target
            shortcut.WorkingDirectory = os.path.dirname(target)
            shortcut.IconLocation = target
            shortcut.Description = "Zebra Label Printer"
            shortcut.save()
        finally:
            if pythoncom is not None:
                pythoncom.CoUninitialize()
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def _log(self, message: str):
        if self.log_text is not None:
            self.log_text.insert("end", message + "\n")
            self.log_text.see("end")
            self.root.update_idletasks()

    def _set_progress_label(self, text: str):
        if self.progress_label is not None:
            # ensure we remove trailing dots so animator can append
            base = text.split(".")[0]
            self.root.after(0, lambda: self.progress_label.config(text=base))

    def _set_progress_value(self, value: int):
        if self.progress is not None:
            self.root.after(0, lambda v=value: self.progress.config(value=v))

    def _stream_download(self, url: str, dest_path: str, chunk_size: int = 1024 * 64):
        """Download a file with progress updates without freezing the UI."""
        with requests.get(url, stream=True, timeout=60) as r:
            r.raise_for_status()
            total = int(r.headers.get('Content-Length', '0'))
            downloaded = 0
            with open(dest_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    if not chunk:
                        continue
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total > 0:
                        pct = int(downloaded * 100 / total)
                        self._set_progress_value(pct)
                    else:
                        # unknown size: bounce the bar subtly
                        cur = int(self.progress['value']) if self.progress else 0
                        self._set_progress_value(min(100, (cur + 3)))

if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap(resource_path("static/icon.ico"))
    app = ZebraLabelPrinterInstaller(root)
    root.mainloop()