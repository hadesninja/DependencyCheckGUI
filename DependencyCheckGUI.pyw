import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
import subprocess
import threading
import os
import requests
import zipfile
import shutil
from datetime import datetime

# Ensure required folders exist
def ensure_folders():
    folders = ["reports", "logs"]
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

# Function to browse source files
def browse_source_files():
    source_files = filedialog.askopenfilenames(title="Select Source Files")
    if source_files:
        source_files_entry.delete(0, tk.END)
        source_files_entry.insert(0, ";".join(source_files))

# Function to browse source folder
def browse_source_folder():
    source_directory = filedialog.askdirectory(title="Select Source Directory")
    if source_directory:
        source_folder_entry.delete(0, tk.END)
        source_folder_entry.insert(0, source_directory)

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
def start_scan():
    ensure_folders()  # Ensure folders exist before running the command

    source_files = source_files_entry.get().split(";")
    source_folder = source_folder_entry.get()
    project_name = project_entry.get()
    api_key = api_key_entry.get()
    output_filename_value = output_filename.get()
    dep_check_path = dep_check_entry.get()

    # Validate mandatory fields
    if not source_files and not source_folder:
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
    output_file_path = os.path.join("reports", f"{output_filename_value}_{timestamp}.html")
    log_file_path = os.path.join("logs", f"{output_filename_value}_{timestamp}.log")

    # Prepare command
    source_paths = source_files + ([source_folder] if source_folder else [])
    source_paths_str = " ".join([f'"{path}"' for path in source_paths])
    command = f'"{dep_check_path}" -s {source_paths_str} --project "{project_name}" --nvdApiKey "{api_key}" --out "{output_file_path}"'

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
                    messagebox.showinfo("Success", f"Scan completed successfully. Report saved to {output_file_path}")
                else:
                    error_message = process.stderr.read()
                    log_file.write(error_message)
                    messagebox.showerror("Error", error_message)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", e.stderr.decode())
        finally:
            # Re-enable the run button after execution
            run_button.config(state=tk.NORMAL)

    # Disable the run button while the command is executing
    run_button.config(state=tk.DISABLED)
    threading.Thread(target=execute_command).start()


# Function to show about information
def show_about():
    messagebox.showinfo("About Developer", "DependencyCheckGUI\n\nVersion 1.0\n\nDeveloper: Vaibhav Patil\n\nThis tool provides User Interface for Windows OS Users to download and run OWASP dependency-check command line tools and generate reports.\n\nIt is an attempt to ease the use of OWASP Dependency Check command line tools with user friendly UI.")

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

            # Clean the dependency-check folder
            clean_dependency_check_folder()

            # Extract the downloaded ZIP file
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(".")

            # Set the dependency-check.bat path automatically
            dep_check_bat_path = os.path.join(os.getcwd(), "dependency-check", "bin", "dependency-check.bat")
            dep_check_entry.delete(0, tk.END)
            dep_check_entry.insert(0, dep_check_bat_path)

            messagebox.showinfo("Download Complete", f"Downloaded and extracted Dependency Check to the current directory.")
            download_popup.destroy()
        except requests.RequestException as e:
            messagebox.showerror("Download Error", f"An error occurred while downloading: {e}")
            download_popup.destroy()

    threading.Thread(target=download_task).start()

# Function to check Dependency Check version
def check_version():
    dep_check_path = dep_check_entry.get()
    if not dep_check_path:
        messagebox.showwarning("Invalid Dependency Check Path", "Please select a valid dependency-check.bat file.")
        return

    command = f'"{dep_check_path}" --version'
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            messagebox.showinfo("Dependency Check Version", stdout.strip())
        else:
            messagebox.showerror("Error", stderr.strip())
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", e.stderr.decode())


# Function to open the version selection window
def open_version_selection_window():
    try:
        response = requests.get("https://api.github.com/repos/jeremylong/DependencyCheck/releases", timeout=10)
        response.raise_for_status()
        releases = response.json()
        versions = [release["tag_name"].lstrip("v") for release in releases]

        if not versions:
            messagebox.showinfo("No Versions Found", "No available versions were found.")
            return

        # Create the new window
        version_window = tk.Toplevel(root)
        version_window.title("Select Dependency Check Version")
        tk.Label(version_window, text="Select a version to download:").grid(row=0, column=0, padx=10, pady=10)

        # Dropdown menu for versions
        selected_version = tk.StringVar(value=versions[0])
        version_dropdown = ttk.Combobox(version_window, textvariable=selected_version, values=versions, state="readonly")
        version_dropdown.grid(row=0, column=1, padx=10, pady=10)

        # Download button
        def on_download():
            version = selected_version.get()
            version_window.destroy()
            download_specific_version(version)

        download_button = tk.Button(version_window, text="Download", command=on_download)
        download_button.grid(row=1, column=0, columnspan=2, pady=10)

    except requests.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch versions: {e}")

# Function to clean the dependency-check folder
def clean_dependency_check_folder():
    dep_check_folder = os.path.join(os.getcwd(), "dependency-check")
    if os.path.exists(dep_check_folder):  # Proceed only if the folder exists
        for item in os.listdir(dep_check_folder):
            item_path = os.path.join(dep_check_folder, item)
            if os.path.isdir(item_path) and item == "data":
                continue  # Skip the data directory
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)  # Remove folder
            elif os.path.isfile(item_path):
                os.remove(item_path)  # Remove file

# Function to download and extract a specific version (reuse logic from the previous implementation,clean the folder before extracting)
def download_specific_version(version):
    download_popup = tk.Toplevel(root)
    download_popup.title(f"Downloading Dependency Check {version}")
    download_progress = tk.DoubleVar()
    progress_bar = ttk.Progressbar(download_popup, variable=download_progress, maximum=100, length=300)
    progress_bar.grid(row=0, column=0, padx=10, pady=10)

    def download_task():
        try:
            download_url = f"https://github.com/jeremylong/DependencyCheck/releases/download/v{version}/dependency-check-{version}-release.zip"
            response = requests.get(download_url, stream=True)
            total_size = int(response.headers.get('content-length', 0))

            if total_size == 0:
                messagebox.showerror("Download Error", "Failed to retrieve the file.")
                download_popup.destroy()
                return

            zip_file_path = f"dependency-check-{version}.zip"
            with open(zip_file_path, "wb") as file:
                downloaded_size = 0
                for data in response.iter_content(chunk_size=1024):
                    file.write(data)
                    downloaded_size += len(data)
                    download_progress.set((downloaded_size / total_size) * 100)
                    download_popup.update_idletasks()

            # Clean the dependency-check folder, preserving the data directory
            clean_dependency_check_folder()

            # Extract the downloaded ZIP file
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(".")
            
            # Set the dependency-check.bat path automatically for the specific version
            dep_check_bat_path = os.path.join(os.getcwd(), "dependency-check", "bin", "dependency-check.bat")
            dep_check_entry.delete(0, tk.END)
            dep_check_entry.insert(0, dep_check_bat_path)

            messagebox.showinfo("Download Complete", f"Downloaded and extracted Dependency Check {version} to the current directory.")
            download_popup.destroy()
        except requests.RequestException as e:
            messagebox.showerror("Download Error", f"An error occurred while downloading: {e}")
            download_popup.destroy()

    threading.Thread(target=download_task).start()


# Create the main window
root = tk.Tk()
root.title("Dependency Check GUI")
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Exit", command=root.quit)

options_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Options", menu=options_menu)
options_menu.add_command(label="Download Latest Dependency Check", command=download_dependency_check)
# Updated options menu to include the new version selection window
options_menu.add_command(label="Download Specific Version", command=open_version_selection_window)


about_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=about_menu)
about_menu.add_command(label="About Us", command=show_about)
about_menu.add_command(label="Check Version of DC Cli tools", command=check_version)

# Create and place the labels and text boxes
tk.Label(root, text="Dependency Check (.bat) Path:").grid(row=0, column=0, padx=10, pady=5)
dep_check_entry = tk.Entry(root, width=50)
dep_check_entry.grid(row=0, column=1, padx=10, pady=5)
browse_dep_button = tk.Button(root, text="Select", command=browse_dependency_check_path)
browse_dep_button.grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Select Files to Scan:").grid(row=1, column=0, padx=10, pady=5)
source_files_entry = tk.Entry(root, width=50)
source_files_entry.grid(row=1, column=1, padx=10, pady=5)
browse_files_button = tk.Button(root, text="Select", command=browse_source_files)
browse_files_button.grid(row=1, column=2, padx=10, pady=5)

tk.Label(root, text="Select Folder to Scan:").grid(row=2, column=0, padx=10, pady=5)
source_folder_entry = tk.Entry(root, width=50)
source_folder_entry.grid(row=2, column=1, padx=10, pady=5)
browse_folder_button = tk.Button(root, text="Select", command=browse_source_folder)
browse_folder_button.grid(row=2, column=2, padx=10, pady=5)

tk.Label(root, text="Enter Project Title:").grid(row=3, column=0, padx=10, pady=5)
project_entry = tk.Entry(root, width=50)
project_entry.grid(row=3, column=1, padx=10, pady=5)
tk.Label(root, text="Enter NVD API Key (Optional):").grid(row=4, column=0, padx=10, pady=5)
api_key_entry = tk.Entry(root, width=50)
api_key_entry.grid(row=4, column=1, padx=10, pady=5)
tk.Label(root, text="Enter Report File name:").grid(row=5, column=0, padx=10, pady=5)
output_filename = tk.Entry(root, width=50)
output_filename.grid(row=5, column=1, padx=10, pady=5)
run_button = tk.Button(root, text="Run Command", command=start_scan)
run_button.grid(row=6, column=0, columnspan=3, pady=10)

output_text = ScrolledText(root, width=80, height=20)
output_text.grid(row=7, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()