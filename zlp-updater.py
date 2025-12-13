import sys
import os
import shutil
import requests
import tempfile
import threading
import tkinter as tk
from tkinter import ttk

from zlp_lib.zlp import resource_path

class UpdateWorker(threading.Thread):
    """Background worker thread that performs the update logic.

    Uses callbacks to report progress and completion back to the Tk UI.
    """

    def __init__(self, app_path, progress_cb, finished_cb):
        super().__init__(daemon=True)
        self.app_path = app_path
        self.progress_cb = progress_cb
        self.finished_cb = finished_cb

    def _progress(self, msg):
        try:
            self.progress_cb(msg)
        except Exception:
            pass

    def run(self):
        try:
            self._progress("Fetching latest release...")

            # Get latest release from GitHub
            api_url = "https://api.github.com/repos/TMarccci/Zebra-Label-Printer/releases/latest"
            response = requests.get(api_url, timeout=30)
            response.raise_for_status()

            release_data = response.json()
            assets = release_data.get('assets', [])

            # Assets we care about
            wanted = {
                "Zebra-Label-Printer.exe": None,
                "zlp-server.exe": None,
                "zlp-uninstaller.exe": None,
                "zlp-updater.exe": None,
            }
            for a in assets:
                name = a.get('name')
                if name in wanted:
                    wanted[name] = a.get('browser_download_url')
                    print(f"Asset URL set for {name}: {wanted[name]}")

            # Validate we found required assets
            missing = [k for k, v in wanted.items() if not v]
            if missing:
                raise RuntimeError(f"Missing assets in release: {', '.join(missing)}")

            temp_dir = tempfile.gettempdir()

            # Download each asset and replace
            for name, url in wanted.items():
                self._progress(f"Downloading {name}...")
                r = requests.get(url, timeout=300)
                r.raise_for_status()

                temp_file = os.path.join(temp_dir, name)
                with open(temp_file, 'wb') as f:
                    f.write(r.content)

                target_file = os.path.join(self.app_path, name)
                print(f"Downloaded {name} to {target_file}")
                self._progress(f"Backing up {name} if exists...")
                if os.path.exists(target_file):
                    shutil.copy2(target_file, target_file + ".bak")

                self._progress(f"Replacing {name}...")
                if name != "zlp-updater.exe":
                    shutil.copy2(temp_file, target_file)
                else:
                    updater_temp_dir = os.path.join(self.app_path, "updater_temp")
                    if not os.path.exists(updater_temp_dir):
                        os.makedirs(updater_temp_dir)
                    shutil.copy2(temp_file, os.path.join(updater_temp_dir, name))

                self._progress(f"Cleaning up {name} temp file...")
                try:
                    os.remove(temp_file)
                except Exception:
                    pass

            # After successful replacement, remove all .bak files for the updated binaries
            for name in wanted.keys():
                bak_path = os.path.join(self.app_path, name + ".bak")
                if os.path.exists(bak_path):
                    try:
                        os.remove(bak_path)
                    except Exception:
                        pass

            self.finished_cb(True, "Update completed successfully!")

        except Exception as e:
            self.finished_cb(False, f"Error: {str(e)}")



class UpdateWindow:
    """Minimal Tkinter UI for the updater with status text and progress bar."""

    def __init__(self, app_path):
        self.app_path = app_path
        self.root = tk.Tk()
        self.root.title("Zebra Label Printer - Update Tool")
        self.root.geometry("400x150+100+100")
        self.root.resizable(False, False)

        # Set icon if available
        try:
            ico = resource_path("static/icon.ico")
            if os.path.exists(ico):
                self.root.iconbitmap(ico)
        except Exception:
            pass

        frame = ttk.Frame(self.root, padding=12)
        frame.pack(fill="both", expand=True)

        self.label_var = tk.StringVar(value="Starting update...")
        self.label = ttk.Label(frame, textvariable=self.label_var, anchor="w")
        self.label.pack(fill="x", pady=(0, 8))

        self.progress = ttk.Progressbar(frame, mode="indeterminate")
        self.progress.pack(fill="x")
        self.progress.start(12)

        # Start worker thread
        self.worker = UpdateWorker(
            app_path=self.app_path,
            progress_cb=lambda msg: self.root.after(0, self._update_progress, msg),
            finished_cb=lambda ok, msg: self.root.after(0, self._on_finished, ok, msg),
        )
        self.worker.start()

    def _update_progress(self, message: str):
        self.label_var.set(message)

    def _on_finished(self, success: bool, message: str):
        self.progress.stop()
        # switch to determinate full bar
        self.progress.config(mode="determinate", maximum=100)
        self.progress['value'] = 100
        self.label_var.set(message)

        # Remove any old .bak files left by previous versions
        if success:
            for name in ["Zebra-Label-Printer.exe", "zlp-server.exe"]:
                bak_path = os.path.join(self.app_path, name + ".bak")
                if os.path.exists(bak_path):
                    try:
                        os.remove(bak_path)
                    except Exception:
                        pass

        # Close after a short delay, then relaunch the app if successful
        def _finish():
            try:
                self.root.destroy()
            finally:
                if success:
                    try:
                        os.startfile(os.path.join(self.app_path, "Zebra-Label-Printer.exe"))
                    except Exception:
                        pass

        self.root.after(2000, _finish)

    def run(self):
        self.root.mainloop()
        


def main():
    # Use fixed install folder
    USER = os.getenv("USERNAME")
    APP_FOLDER = f"C:\\Users\\{USER}\\Zebra Label Printer"

    if not os.path.exists(APP_FOLDER):
        print(f"Error: Folder not found: {APP_FOLDER}")
        sys.exit(1)

    window = UpdateWindow(APP_FOLDER)
    window.run()


if __name__ == "__main__":
    main()