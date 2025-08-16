# Change Log

## [Version 1.2](https://github.com/hadesninja/DependencyCheckGUI/releases/tag/v1.2) - 2025-01-05

### Added
- **Preferences Menu** under File:
  - **Set NVD API Key**: Added a feature to configure or update the NVD API key.
- **Tools Menu Enhancements**:
  - **CVE Details**: Users can now enter single or multiple CVE IDs (comma-separated) and fetch detailed information.
  - **Jar Vulnerability Finder**: Added a feature to select a JAR file and fetch reported CVEs for it.

### Changed
- **UI Update**: Improved and optimized the user interface using PyQt5 for a smoother experience.
- **Menu Structure Update**: Now only three main menus exist: **File**, **Tools**, and **Help**.
- **Menu Relocations**:
  - **Purge NVD Data** moved to **File → Options → Purge NVD Data**.
  - **Update DC Tools** moved to the **Help** menu.

### Fixed
- General bug fixes and performance improvements for better stability.



## [Version 1.1](https://github.com/hadesninja/DependencyCheckGUI/releases/tag/v1.1) - 2025-01-05

### Added
- Added a **File menu** with the following features:
  - **Open Reports Folder**: Opens the "Reports" folder from the current directory in the file explorer.
  - **Open Logs Folder**: Opens the "Logs" folder from the current directory in the file explorer.
  - **Exit Program**: Allows the user to exit the program through the File menu.
- Added an **Options Menu** with the following tools:
  - **Update DC tools to the latest version**: Provides an option to download and update the Dependency-Check tools to latest version.
  - **Download Specific Versions**: Allows the user to download specific versions of the Dependency-Check tools.
  - **Purge NVD Data**: Provides a tool to purge the National Vulnerability Database (NVD) data.
- Added a **Help Menu** with the following options:
  - **Check Version of DC Tools**: Displays information about the current version of the Dependency-Check tools.
  - **About the Application**: Provides general information about the application.
- **Select Files Feature**: Enables users to choose specific files (such as .jar, .js, .exe, .zip, and others) for dependency scanning.
- **Dependency Check Folder Cleanup**: Added logic to clean up old versions of Dependency-Check tools when a new or specific version is downloaded, while preserving NVD data.
- **NVD API Key Information Popup**: Introduced a popup window that provides detailed information about the NVD API key wehn click on info button. The popup includes instructions on how to request an API key from the National Vulnerability Database (NVD).

### Changed
- **Button Label Update**: Changed the button label from **"Run Command"** to **"Start Scan"** for better clarity and alignment with functionality.
- **Entry Labels Update**: Changed the labels of all entry fields to more appropriate and descriptive names to improve user experience and clarity.

### Fixed
- **Button State Change**: Added feature to disable the button until the current scan finishes once clicked , preventing multiple clicks which causes errors.

### Removed
- Removed the **Output report filename entry** field.
  - Now, the **project name** is used automatically to save both the report and log files, simplifying the file management process.
- Removed the **Browse Dependency-Check.bat** field:
  - Removed the need for users to select the `dependency-check.bat` file every time the application is run.
  - Now path to the `dependency-check.bat` file is now set by default, streamlining the process.



## [Version 1.0](https://github.com/hadesninja/DependencyCheckGUI/releases/tag/v1.0) (Initial Release) - 2024-12-21

### Added
- **GUI for OWASP Dependency-Check Scans**: A new graphical user interface to facilitate running Dependency-Check scans.
- **Browsing for Source Directory and Dependency-Check.bat**: Added the ability to browse for the source directory and the `dependency-check.bat` file.
- **Real-Time Log Display**: Integrated functionality to run Dependency-Check scans and display logs in real-time.
- **Folder Creation**: Introduced the `ensure_folders` function to automatically check for and create the required reports and logs folders.
- **Dynamic Log Filename**: The log filename now includes both the report's filename and a timestamp (e.g., `output_20231221_123456.log`).
- **Timestamp Generation**: Utilized `datetime.now().strftime` to format the timestamp for the log file.
- **File Path Management**: Improved file path management by using `os.path.join` to create report and log paths more cleanly.
- **User Feedback**: Enhanced feedback with success and error messages detailing the paths of the generated report and logs.
- **Mandatory Fields Validation**: Added checks to ensure the Report Title (`project_entry`) and Output Report Filename (`output_filename`) fields are not empty.
- **Warning for Empty Fields**: Display a warning message if the Project Report Title and Output Report Filename fields are empty.
- **Error Handling**: Error messages prompt the user to fill in mandatory fields with detailed guidance.
- **Mandatory Fields Implementation**: Smoother validation process for mandatory fields before executing commands.
- **Dependency-Check Update Option**: Included an option to download and update to the latest version of Dependency-Check.

### Changed
- **Report and Log Storage**: Updated the `run_command` function to store generated reports in the `reports` folder and logs in the `logs` folder.

