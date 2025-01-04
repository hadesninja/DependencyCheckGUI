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

# Function to browse source path
def browse_source_path():
    source_directory = filedialog.askdirectory(title="Select folder to scan")
    if source_directory:
        source_entry.delete(0, tk.END)
        source_entry.insert(0, source_directory)

# Function to browse files to scan
def browse_files():
    file_types = [
        ("Supported files", "*.jar *.js *.lock *.h *.nuspec *.csproj *.vbproj *.zip *.ear *.war *.sar *.apk *.nupkg *.exe *.dll"),
        ("All files", "*.*")
    ]
    files = filedialog.askopenfilenames(
        title="Select Files",
        filetypes=file_types
    )
    if files:
        files_entry.delete(0, tk.END)
        files_entry.insert(0, ";".join(files))

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

# Function to check Dependency Check version
def check_version():
    dep_check_path = os.path.join("dependency-check", "bin", "dependency-check.bat")
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
            
                    # Clean the dependency-check folder, preserving the data directory
                    clean_dependency_check_folder()

            # Extract the zip file
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(".")
            
            # Delete the zip file after extraction
            if os.path.exists(zip_file_path):
                os.remove(zip_file_path)
            
            messagebox.showinfo("Download Complete", f"Downloaded and extracted Dependency Check to the current directory.")
            download_popup.destroy()
        except requests.RequestException as e:
            messagebox.showerror("Download Error", f"An error occurred while downloading: {e}")
            download_popup.destroy()

    threading.Thread(target=download_task).start()

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

# Function to download and extract a specific version (reuse logic from the previous implementation, clean the folder before extracting)
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
            

            # Delete the zip file after extraction
            if os.path.exists(zip_file_path):
                os.remove(zip_file_path)

            messagebox.showinfo("Download Complete", f"Downloaded and extracted Dependency Check {version} to the current directory.")
            download_popup.destroy()
        except requests.RequestException as e:
            messagebox.showerror("Download Error", f"An error occurred while downloading: {e}")
            download_popup.destroy()

    threading.Thread(target=download_task).start()



# Function to run the dependency-check command
def start_scan():
    ensure_folders()  # Ensure folders exist before running the command

    # Disable the Start Scan button
    run_button.config(state=tk.DISABLED)

    source_path = source_entry.get()
    files = files_entry.get().split(";")
    project_name = project_entry.get()
    api_key = api_key_entry.get()
    output_filename_value = output_filename.get()
    dep_check_path = os.path.join("dependency-check", "bin", "dependency-check.bat")

    # Validate mandatory fields
    if not source_path and not files:
        messagebox.showwarning("Invalid Input", "Please select a valid source path or files to scan.")
        run_button.config(state=tk.NORMAL)  # Re-enable the button
        return

    if not os.path.exists(dep_check_path):
        response = messagebox.askyesno("Dependency Check Not Found", "dependency-check.bat not found. Do you want to download the latest version?")
        if response:
            download_dependency_check()
        run_button.config(state=tk.NORMAL)  # Re-enable the button
        return

    if not project_name:
        messagebox.showwarning("Missing Report Title", "The Report Title field is mandatory.")
        run_button.config(state=tk.NORMAL)  # Re-enable the button
        return

    if not output_filename_value:
        messagebox.showwarning("Missing Output Filename", "The Output Report Filename field is mandatory.")
        run_button.config(state=tk.NORMAL)  # Re-enable the button
        return


    # Prepare file paths
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file_path = os.path.join("reports", f"{output_filename_value}_{timestamp}.html")
    log_file_path = os.path.join("logs", f"{output_filename_value}_{timestamp}.log")

    # Prepare command
    command = f'"{dep_check_path}"'
    # Add source_path argument if it's not empty
    if source_path:
        command += f' -s "{source_path}"'
    # Add each file argument if files is not empty
    for file in files:
        if file:  # Ensure file is not empty
            command += f' -s "{file}"'
    # Add other required arguments
    command += f' --project "{project_name}" --nvdApiKey "{api_key}" --out "{output_file_path}"'


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
            run_button.config(state=tk.NORMAL)  # Re-enable the button after execution

    threading.Thread(target=execute_command).start()

# Function to show about information
def show_about():
    messagebox.showinfo("About Developer", "DependencyCheckGUI\n\nVersion 1.1\n\nDeveloper: Vaibhav Patil"
                        "\n\nThis tool provides User Interface for Windows OS Users to download and run OWASP dependency-check command line tools and generate reports."
                        "\n\nIt is an attempt to ease the use of OWASP Dependency Check command line tools with user friendly UI.")

# Function to exit the program
def exit_program():
    root.quit()

# Create the main window
root = tk.Tk()
root.title("Dependency Check Runner")
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Exit", command=exit_program)

# Options menu
options_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Options", menu=options_menu)
options_menu.add_command(label="Update DependencyCheck Tools", command=download_dependency_check)
# Updated options menu to include the new version selection window
options_menu.add_command(label="Download Specific Version", command=open_version_selection_window)

# About menu
help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="Check Version of DC Tools", command=check_version)
help_menu.add_command(label="About Us", command=show_about)


# Create and place the labels and text boxes
tk.Label(root, text="Select folder to scan:").grid(row=0, column=0, padx=10, pady=5)
source_entry = tk.Entry(root, width=50)
source_entry.grid(row=0, column=1, padx=10, pady=5)
browse_button = tk.Button(root, text="Select", command=browse_source_path)
browse_button.grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Select files to scan:").grid(row=1, column=0, padx=10, pady=5)
files_entry = tk.Entry(root, width=50)
files_entry.grid(row=1, column=1, padx=10, pady=5)
browse_files_button = tk.Button(root, text="Select", command=browse_files)
browse_files_button.grid(row=1, column=2, padx=10, pady=5)

tk.Label(root, text="Project Report Title:").grid(row=2, column=0, padx=10, pady=5)
project_entry = tk.Entry(root, width=50)
project_entry.grid(row=2, column=1, padx=10, pady=5)
tk.Label(root, text="NVD API Key (Optional):").grid(row=3, column=0, padx=10, pady=5)
api_key_entry = tk.Entry(root, width=50)
api_key_entry.grid(row=3, column=1, padx=10, pady=5)
tk.Label(root, text="Output Report Filename:").grid(row=4, column=0, padx=10, pady=5)
output_filename = tk.Entry(root, width=50)
output_filename.grid(row=4, column=1, padx=10, pady=5)
run_button = tk.Button(root, text="Start Scan", command=start_scan)
run_button.grid(row=5, column=0, columnspan=3, pady=10)

output_text = ScrolledText(root, width=80, height=20)
output_text.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()
