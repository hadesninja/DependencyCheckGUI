# DependencyCheckGUI

This tool provides User Interface for Windows OS Users to download and run OWASP dependency-check command line tools and generate reports. It is an attempt to ease the use of OWASP Dependency Check command line tools with user friendly UI.

## Features
The provided code implements a GUI application to facilitate running the OWASP Dependency Check tool. Here's a breakdown of the key functionalities:
Browse for Source Path: The browse_source_path function opens a directory selection dialog for the user to select the source directory. The selected path is then inserted into the source_entry text field.

Download Latest Dependency Check: The download_dependency_check function downloads the latest version of the Dependency Check tool from GitHub, shows a progress bar during the download, and extracts the downloaded zip file to the current directory.

Browse for Dependency Check Path: The browse_dependency_check_path function opens a file selection dialog for the user to select the dependency-check.bat file. The selected file path is then inserted into the dep_check_entry text field.

Run Dependency Check Command: The start_scan function validates the user inputs, constructs the command to run the Dependency Check tool, and executes it in a separate thread. The output and errors are logged to a file and displayed in the ScrolledText widget.

Ensure Required Folders Exist: The application ensures existence of "reports" and "logs" directories and creates them if they do not exist when click Scan.