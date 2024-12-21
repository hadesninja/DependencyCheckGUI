import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
import subprocess
import threading
import os
import requests
import zipfile
from datetime import datetime

# Ensure required folders exist
def ensure_folders():
    folders = ["reports", "logs"]
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

# Function to browse source path
def browse_source_path():
    source_directory = filedialog.askdirectory(title="Select Source Directory")
    if source_directory:
        source_entry.delete(0, tk.END)
        source_entry.insert(0, source_directory)

# Function to browse dependency-check.bat path
def browse_dependency_check_path():
    current_directory = os.getcwd()
    dep_check_file = filedialog.askopenfilename(
        title="Select dependency-check.bat", 
        filetypes=[("Batch files", "*.bat")],
        initialdir=current_directory
    )
    if dep_check_file:
        dep_check_entry.delete(0, tk.END)
        dep_check_entry.insert(0, dep_check_file)

# Function to run the dependency-check command
def run_command():
    ensure_folders()  # Ensure folders exist before running the command

    source_path = source_entry.get()
    project_name = project_entry.get()
    api_key = api_key_entry.get()
    output_filename_value = output_filename.get()
    dep_check_path = dep_check_entry.get()

    # Validate mandatory fields
    if not source_path:
        messagebox.showwarning("Invalid Source Path", "Please select a valid source path.")
        return

    if not dep_check_path:
        messagebox.showwarning("Invalid Dependency Check Path", "Please select a valid dependency-check.bat file.")
        return

    if not project_name:
        messagebox.showwarning("Missing Report Title", "The Report Title field is mandatory.")
        return

    if not output_filename_value:
        messagebox.showwarning("Missing Output Filename", "The Output Report Filename field is mandatory.")
        return

    # Prepare file paths
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file_path = os.path.join("reports", f"{output_filename_value}.html")
    log_file_path = os.path.join("logs", f"{output_filename_value}_{timestamp}.log")

    # Prepare command
    command = f'"{dep_check_path}" -s "{source_path}" --project "{project_name}" --nvdApiKey "{api_key}" --out "{output_file_path}"'

    def execute_command():
        try:
            with open(log_file_path, "w") as log_file:
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                for line in process.stdout:
                    log_file.write(line)
                    output_text.insert(tk.END, line)
                    output_text.see(tk.END)
                process.wait()
                if process.returncode == 0:
                    messagebox.showinfo("Success", f"Command executed successfully. Report saved to {output_file_path}")
                else:
                    error_message = process.stderr.read()
                    log_file.write(error_message)
                    messagebox.showerror("Error", error_message)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", e.stderr.decode())

    threading.Thread(target=execute_command).start()

# Function to show about information
def show_about():
    messagebox.showinfo("About Developer", "Developer: Vaibhav Patil\n\nDependencyCheckGUI: v1.1\n\nThis tool provides User Interface for Windows OS Users to download and run OWASP dependency-check command line tools and generate reports.\n\nIt is an attempt to ease the use of OWASP Dependency Check command line tools with user friendly UI.")

# Function to download the latest version of Dependency Check
def download_dependency_check():
    download_popup = tk.Toplevel(root)
    download_popup.title("Downloading Dependency Check")
    download_progress = tk.DoubleVar()
    progress_bar = ttk.Progressbar(download_popup, variable=download_progress, maximum=100, length=300)
    progress_bar.grid(row=0, column=0, padx=10, pady=10)

    def download_task():
        try:
            version_response = requests.get("https://jeremylong.github.io/DependencyCheck/current.txt", timeout=10)
            version_response.raise_for_status()
            version = version_response.text.strip()
            download_url = f"https://github.com/jeremylong/DependencyCheck/releases/download/v{version}/dependency-check-{version}-release.zip"
            response = requests.get(download_url, stream=True)
            total_size = int(response.headers.get('content-length', 0))

            if total_size == 0:
                messagebox.showerror("Download Error", "Failed to retrieve the file.")
                download_popup.destroy()
                return

            zip_file_path = "dependency-check.zip"
            with open(zip_file_path, "wb") as file:
                downloaded_size = 0
                for data in response.iter_content(chunk_size=1024):
                    file.write(data)
                    downloaded_size += len(data)
                    download_progress.set((downloaded_size / total_size) * 100)
                    download_popup.update_idletasks()

            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(".")
            messagebox.showinfo("Download Complete", f"Downloaded and extracted Dependency Check to the current directory.")
            download_popup.destroy()
        except requests.RequestException as e:
            messagebox.showerror("Download Error", f"An error occurred while downloading: {e}")
            download_popup.destroy()

    threading.Thread(target=download_task).start()

# Create the main window
root = tk.Tk()
root.title("Dependency Check Runner")
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)
download_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Download", menu=download_menu)
download_menu.add_command(label="Download Latest Dependency Check", command=download_dependency_check)
about_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="About", menu=about_menu)
about_menu.add_command(label="About Us", command=show_about)

# Create and place the labels and text boxes
tk.Label(root, text="Source lib folder:").grid(row=0, column=0, padx=10, pady=5)
source_entry = tk.Entry(root, width=50)
source_entry.grid(row=0, column=1, padx=10, pady=5)
browse_button = tk.Button(root, text="Browse", command=browse_source_path)
browse_button.grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Dependency Check (.bat) Path:").grid(row=1, column=0, padx=10, pady=5)
dep_check_entry = tk.Entry(root, width=50)
dep_check_entry.grid(row=1, column=1, padx=10, pady=5)
browse_dep_button = tk.Button(root, text="Browse", command=browse_dependency_check_path)
browse_dep_button.grid(row=1, column=2, padx=10, pady=5)

tk.Label(root, text="Project Report Title:").grid(row=2, column=0, padx=10, pady=5)
project_entry = tk.Entry(root, width=50)
project_entry.grid(row=2, column=1, padx=10, pady=5)
tk.Label(root, text="NVD API Key (Optional):").grid(row=3, column=0, padx=10, pady=5)
api_key_entry = tk.Entry(root, width=50)
api_key_entry.grid(row=3, column=1, padx=10, pady=5)
tk.Label(root, text="Output Report Filename:").grid(row=4, column=0, padx=10, pady=5)
output_filename = tk.Entry(root, width=50)
output_filename.grid(row=4, column=1, padx=10, pady=5)
run_button = tk.Button(root, text="Run Command", command=run_command)
run_button.grid(row=5, column=0, columnspan=3, pady=10)

output_text = ScrolledText(root, width=80, height=20)
output_text.grid(row=6, column=0, columnspan=3, padx=10, pady=10)
root.mainloop()
