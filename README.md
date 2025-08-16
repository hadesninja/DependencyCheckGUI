# DependencyCheckGUI

**DependencyCheckGUI** is a graphical user interface (GUI) tool for running the OWASP Dependency Check command-line tools to scan and generate software dependency reports. The tool simplifies the interaction with Dependency-Check, which identifies known vulnerabilities in software libraries. This GUI is designed for Windows users but should work on other platforms with minor modifications.

## Features

#### 1. **Dependency Check Integration**
   - Download and install the latest version of Dependency-Check.
   - Purge NVD (National Vulnerability Database) data using Dependency-Check tools.
   - Check the current version of Dependency-Check installed.
   - Option to download specific versions of Dependency-Check from the official repository.

#### 2. **Folder and File Selection**
   - **Browse Folder**: Allows users to select a folder to scan for dependencies.
   - **Browse Files**: Enables users to choose specific files (such as `.jar`, `.exe`, `.zip`, and others) for dependency scanning.

#### 3. **Customizable Reports**
  - Users can define a **project name** for reports and log files.
  - The **project name** is used automatically for naming the report and log files, improving the organization and management of generated files.

#### 4. **Scan Execution**
   - **Start Scan**: After selecting the files or folders, users can initiate the Dependency-Check scan by clicking the "Start Scan" button.
   - The scan runs in a background thread and outputs log details in a scrollable text field.
   - Users can also provide an optional **NVD API key** for enhanced integration with the National Vulnerability Database (NVD). An **Info button** is available next to the NVD API key entry field. When clicked, it provides useful information on how to obtain and use an NVD API key. 

#### 5. **NVD Data Purging**
   - **Purge NVD Data**: Clears local NVD data, which may need to be refreshed occasionally to stay up-to-date with vulnerabilities.
   
#### 6. **Download Latest Dependency-Check**
   - Automatically download and install the latest version of Dependency-Check, or select specific versions for download.
   - A progress bar shows the download and extraction status.

#### 7. **Menu Bar Options**
   - **File**: Contains basic file operations such as  "Open Reports folder","Open logs folder" and "Exit".
     - **Open Reports Folder**: Opens the "Reports" folder located in the current working directory in the default file explorer.
     - **Open Logs Folder**: Opens the "Logs" folder located in the current working directory in the default file explorer.
     - **Exit**: Exits the application.
   - **Options**: Includes tools for updating Dependency-Check tools, downloading specific versions, and purging NVD data.
     - **Update DC Tools to Latest Version**: Allows the user to update the Dependency-Check tools to the latest version.
     - **Download Specific Versions**: Allows the user to download a specific version of the Dependency-Check tools.
     - **Purge NVD Data**: Provides an option to purge the National Vulnerability Database (NVD) data, clearing stored vulnerability information.
   - **Help**: Provides information on the current version of Dependency-Check tools and about the application.
     - **Check Version of DC Tools**: Displays information about the current version of the Dependency-Check tools being used.
     - **About Us**: Provides general information about the application, including its purpose and features.


## Usage

#### **Running the Program**
To run the program:

**Using .exe File:**

Download the .exe file from the release section.
Simply double-click to run the application, and the GUI will open, ready to use.

**Using the Python Script:**

Clone or download the repository.
Ensure Python 3.6+ and the required libraries are installed.
Execute the script:

`python DependencyCheckGUI.py`

This will open the GUI window, allowing you to start scanning for vulnerabilities in your dependencies.




## How It Works

**Scanning:** The tool uses the dependency-check.bat script from OWASP Dependency-Check to perform the actual vulnerability scan. Users can input a folder or files to be scanned and configure the output report filename.

**Download Process:** If Dependency-Check is not installed, users will be prompted to download it. The download and extraction process is shown via a progress bar.

**Purge NVD Data:** The tool allows you to clear local NVD data to ensure you’re using up-to-date vulnerability information. If no data is available to purge, the tool will notify the user.

## Requirements

#### Java Version

Minimum Java Version: Java 11

#### Internet Access

DependencyCheckGUI requires access to several externally hosted resources wuch as Dependency Check command line tools and NVD data.

#### **For .exe Release Version**:
If you are using the compiled `.exe` version of DependencyCheckGUI, you can skip the installation of Python dependencies. Simply download and run the `.exe` file, and you can start using the program immediately.

#### **For Source Code (Python Version)**:
If you are running the Python source code, ensure that Python 3.6+ and the following Python libraries are installed:

**Python**: Ensure you have Python 3.6+ installed.

**Python Libraries**:
   - `pyqt5` (for the GUI)
   - `requests` (for downloading files)
   - `subprocess` (for executing system commands)
   - `shutil` and `os` (for file and directory manipulation)
   - `zipfile` (for handling ZIP file extraction)
   - `threading` (to handle background tasks)
   
You can install the necessary libraries using `pip`:

`pip install requests`

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/DependencyCheckGUI.git


## Troubleshooting

- **Dependency-Check Not Found:** If the tool can't find dependency-check.bat, it will prompt the user to download it.

- **Permissions:** Ensure that the program has sufficient permissions to read/write files and folders, especially in the "reports" and "logs" directories.

- **Network Issues:** If the tool can't download the latest version of Dependency-Check, ensure your network connection is stable and the server is reachable.

- **Purging NVD Data:** If NVD data cannot be purged because it doesn't exist, the program will notify the user that there is no data to purge.

## License
This project is licensed under the MIT License. See the [LICENSE](https://github.com/hadesninja/DependencyCheckGUI?tab=MIT-1-ov-file#readme) file for details.

## Acknowledgements

- **OWASP Dependency-Check:** [OWASP Dependency-Check](https://owasp.org/www-project-dependency-check/)
- **Tkinter:** Tkinter is used for creating the graphical user interface (GUI).
- **Requests:** Used for downloading files.
- **GitHub API:** Used to fetch available versions of 
- **Dependency-Check** from the official repository.
- **Python:** This tool is developed using Python for cross-platform compatibility.
