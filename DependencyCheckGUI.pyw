import os
import re
import shutil
import subprocess
import threading
import datetime
import requests
import zipfile
import xml.etree.ElementTree as ET
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from fetch_cve_details import CVEDetailsRetriever
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QTextEdit, QMenuBar, QAction, QFileDialog

from jar_vulnerability_finder import JarVulnerabilityScanner


class DependencyCheckGUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Dependency Check GUI")
        layout = QVBoxLayout()

        # Menu Bar - File Menu
        self.menu_bar = QMenuBar(self)
        self.file_menu = self.menu_bar.addMenu("File")

        # Open Folder Actions
        open_dc_reports_action = QAction("Open DC Reports", self)
        open_dc_reports_action.triggered.connect(self.open_dc_reports)
        self.file_menu.addAction(open_dc_reports_action)

        open_logs_action = QAction("Open Logs", self)
        open_logs_action.triggered.connect(self.open_logs)
        self.file_menu.addAction(open_logs_action)

        open_sca_jar_templates_action = QAction("Open SCA_Jar_Templates", self)
        open_sca_jar_templates_action.triggered.connect(self.open_sca_jar_templates)
        self.file_menu.addAction(open_sca_jar_templates_action)

        # Settings Menu (Preferences)
        self.options_menu = self.file_menu.addMenu("Options")
        self.set_api_key_action = QAction("Purge NVD data", self)
        self.set_api_key_action.triggered.connect(self.purge_NVD_data)
        self.options_menu.addAction(self.set_api_key_action)

        # Settings Menu
        self.preferences_menu = self.file_menu.addMenu("Preferences")
        self.set_api_key_action = QAction("Set NVD API Key", self)
        self.set_api_key_action.triggered.connect(self.set_nvd_api_key)
        self.preferences_menu.addAction(self.set_api_key_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(QApplication.quit)
        self.file_menu.addAction(exit_action)

        # === TOOLS MENU ===
        tools_menu = self.menu_bar.addMenu("Tools")

        # Load Plugins action
        load_plugins_action = QAction("CVE Details", self)
        load_plugins_action.triggered.connect(self.fetch_cve_details)
        tools_menu.addAction(load_plugins_action)

        # Action for "Jar Vulnerability Finder"
        load_plugins_action = QAction("Jar Vulnerability Finder", self)
        load_plugins_action.triggered.connect(self.jar_vulnerability_finder)
        tools_menu.addAction(load_plugins_action)

        # Menu Bar - Help Menu
        self.help_menu = self.menu_bar.addMenu("Help")
        self.download_dc_action = QAction("Update DC Tools", self)
        self.download_dc_action.triggered.connect(self.download_dependency_check)
        self.help_menu.addAction(self.download_dc_action)

        self.check_dc_version = QAction("Check DC Tools Version", self)
        self.check_dc_version.triggered.connect(self.check_dctools_version)
        self.help_menu.addAction(self.check_dc_version)

        self.about_action = QAction("About", self)
        self.about_action.triggered.connect(self.show_about_dialog)
        self.help_menu.addAction(self.about_action)

        layout.setMenuBar(self.menu_bar)

        # Folder selection
        folder_layout = QHBoxLayout()
        self.folder_label = QLabel("Select folder to scan:")
        folder_layout.addWidget(self.folder_label)
        self.folder_entry = QLineEdit()
        folder_layout.addWidget(self.folder_entry)
        self.folder_button = QPushButton("Select")
        self.folder_button.clicked.connect(self.browse_source_path)
        folder_layout.addWidget(self.folder_button)
        layout.addLayout(folder_layout)

        # File selection
        file_layout = QHBoxLayout()
        self.file_label = QLabel("Select files to scan:")
        file_layout.addWidget(self.file_label)
        self.file_entry = QLineEdit()
        file_layout.addWidget(self.file_entry)
        self.file_button = QPushButton("Select")
        self.file_button.clicked.connect(self.browse_files)
        file_layout.addWidget(self.file_button)
        layout.addLayout(file_layout)

        # Project Name
        project_layout = QHBoxLayout()
        self.project_label = QLabel("Project Name:")
        project_layout.addWidget(self.project_label)
        self.project_entry = QLineEdit()
        project_layout.addWidget(self.project_entry)
        layout.addLayout(project_layout)

        # Report format dropdown
        format_layout = QHBoxLayout()
        self.format_label = QLabel("Report Format:")
        format_layout.addWidget(self.format_label)
        self.format_dropdown = QComboBox()
        self.format_dropdown.addItems(["HTML", "CSV", "XML"])
        format_layout.addWidget(self.format_dropdown)
        layout.addLayout(format_layout)

        # Start the scan button
        self.scan_button = QPushButton("Start Scan")
        self.scan_button.clicked.connect(self.start_scan)
        layout.addWidget(self.scan_button)

        # Output text
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text)

        self.setLayout(layout)

        # Connect the entry fields to handle clearing and enabling/disabling buttons
        self.folder_entry.textChanged.connect(self.check_folder_entry)
        self.file_entry.textChanged.connect(self.check_file_entry)

        self.ensure_folders()

    def browse_source_path(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_entry.setText(folder)
            self.file_button.setDisabled(True)  # Disable file selection button

    def browse_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files")
        if files:
            self.file_entry.setText(", ".join(files))
            self.folder_button.setDisabled(True)  # Disable folder selection button

    def check_folder_entry(self):
        """Check if the folder entry is cleared and enable the file button if so"""
        if not self.folder_entry.text().strip():  # If the folder entry is empty
            self.file_button.setEnabled(True)  # Re-enable file selection button

    def check_file_entry(self):
        """Check if the file entry is cleared and enable the folder button if so"""
        if not self.file_entry.text().strip():  # If the file entry is empty
            self.folder_button.setEnabled(True)  # Re-enable folder selection button

    # purse nvd data
    def purge_NVD_data(self):
        """
        Function to purge NVD data using Dependency-Check.
        If Dependency-Check is not found, prompt user to download it.
        """
        dep_check_path = os.path.join("dependency-check", "bin", "dependency-check.bat")

        # Check if dependency-check.bat exists
        if not os.path.exists(dep_check_path):
            response = QMessageBox.question(
                self,
                "Dependency Check Not Found",
                "The 'dependency-check.bat' file could not be found.\n\nWould you like to download the latest version?",
                QMessageBox.Ok | QMessageBox.Cancel,
                QMessageBox.Ok
            )

            if response == QMessageBox.Ok:
                self.download_dependency_check()  # You need to define this function separately
            return

        # Purge NVD data
        command = f'"{dep_check_path}" --purge'

        try:
            print("Purging NVD data...")
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)

            if "Unable to purge database; the database file does not exist" in result.stderr:
                QMessageBox.information(self, "No Data to Purge", "No NVD data found to purge.")
            elif result.returncode == 0:
                QMessageBox.information(self, "Purge Successful", "NVD data has been successfully purged.")
            else:
                QMessageBox.critical(self, "Purge Failed", f"Failed to purge NVD data:\n{result.stderr}")

        except subprocess.CalledProcessError as e:
            if "Unable to purge database; the database file does not exist" in e.stderr:
                QMessageBox.information(self, "No Data to Purge", "No NVD data found to purge.")
            else:
                QMessageBox.information(self, "No Data to Purge", "No NVD data found to purge.")

    def jar_vulnerability_finder(self):
        # Create and show the Jar Vulnerability Finder window
        self.jar_vuln_window = JarVulnerabilityScanner()  # Instantiate the vulnerability finder
        self.jar_vuln_window.show()


    def open_folder(self, folder_name):
        """Open the folder in the system's default file explorer."""
        folder_path = os.path.join(os.getcwd(), folder_name)
        if os.path.exists(folder_path):
            if os.name == 'nt':  # For Windows
                subprocess.run(['explorer', folder_path])
            elif os.name == 'posix':  # For Linux/MacOS
                subprocess.run(['xdg-open', folder_path])
        else:
            QtWidgets.QMessageBox.warning(self, "Folder Not Found", f"{folder_name} folder does not exist.")

    def open_dc_reports(self):
        self.open_folder("Reports")

    def open_logs(self):
        self.open_folder("Logs")

    def open_sca_jar_templates(self):
        self.open_folder("SCA_Jar_Templates")

    def show_about_dialog(self):
        QtWidgets.QMessageBox.about(
            self,
            "About Dependency Check GUI",
            (
                "<h3>Dependency Check GUI</h3>"
                "<p><b>Version:</b> 1. 2</p>"
                "<p>A lightweight GUI interface for managing OWASP Dependency Check scans.</p>"
                "<p>This tool provides a user-friendly interface for Windows users to download and run OWASP Dependency Check command-line tools and generate reports.</p>"
                "<p>It simplifies the use of Dependency Check by abstracting the complexity of the command-line.</p>"
                "<p><b>Developed by:</b> Vaibhav Patil</p>"
            )
        )

    def fetch_cve_details(self):
        self.cve_window = CVEDetailsRetriever()
        self.cve_window.show()

    def check_dctools_version_startup(parent: QWidget):
        dep_check_path = os.path.join("dependency-check", "bin", "dependency-check.bat")

        # If dependency-check.bat doesn't exist
        if not os.path.exists(dep_check_path):
            reply = QMessageBox.question(
                parent,
                "Dependency Check Not Found",
                "The 'dependency-check.bat' file could not be found.\nYou can download the latest version of Dependency-Check.\n\nDo you want to download it?",
                QMessageBox.Ok | QMessageBox.Cancel
            )

            if reply == QMessageBox.Ok:
                parent.download_dependency_check()
            return

        try:
            # Get local version by running dependency-check.bat --version
            result = subprocess.run([dep_check_path, "--version"], capture_output=True, text=True, shell=True)
            local_version_output = result.stdout.strip()

            # Extract version number (assuming output like "Dependency-Check Core version 8.4.0")
            match = re.search(r"version (\d+\.\d+\.\d+)", local_version_output)
            if match:
                local_version = match.group(1)
            else:
                local_version = None

            # Fetch latest version
            version_url = "https://dependency-check.github.io/DependencyCheck/current.txt"
            response = requests.get(version_url)
            if response.status_code == 200:
                latest_version = response.text.strip()
            else:
                latest_version = None

            # Compare versions
            if local_version and latest_version:
                if local_version != latest_version:
                    reply = QMessageBox.question(
                        parent,
                        "Update Available",
                        f"A newer version of Dependency-Check Tools is available.\n\nCurrent version: {local_version}\nLatest version: {latest_version}\n\nDo you want to download the latest version?",
                        QMessageBox.Ok | QMessageBox.Cancel
                    )

                    if reply == QMessageBox.Ok:
                        parent.download_dependency_check()
                else:
                    # Optional: Inform user it's up to date
                    pass
            else:
                parent.append_output("Could not determine local or latest Dependency-Check version.")

        except Exception as e:
            parent.append_output(f"Error checking Dependency-Check version: {str(e)}")

    def check_dctools_version(parent: QWidget):
        # Path to dependency-check.bat
        dep_check_path = os.path.join("dependency-check", "bin", "dependency-check.bat")

        # If dependency-check.bat doesn't exist
        if not os.path.exists(dep_check_path):
            reply = QMessageBox.question(
                parent,
                "Dependency Check Not Found",
                "The 'dependency-check.bat' file could not be found.\nYou can download the latest version of Dependency-Check.\n\nDo you want to download it?",
                QMessageBox.Ok | QMessageBox.Cancel
            )

            if reply == QMessageBox.Ok:
                parent.download_dependency_check()  # ✅ Call the method from the main window
            return

        # Execute the version check
        command = f'"{dep_check_path}" --version'
        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                QMessageBox.information(parent, "Dependency Check Version", stdout.strip())
            else:
                QMessageBox.critical(parent, "Error", stderr.strip())
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(parent, "Error", str(e))


    def ensure_folders(self):
        for folder in ("Reports", "Logs", "SCA_Jar_Templates", "Backups", "dependency-check"):
            os.makedirs(folder, exist_ok=True)

    def browse_source_path(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder to Scan")
        if folder:
            self.folder_entry.setText(folder)
            self.file_entry.clear()  # Clear file entry when the folder is selected

    def browse_files(self):
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Select Files to Scan", "",
                                                          "Supported files (*.jar *.js *.lock *.h *.nuspec *.csproj *.vbproj *.zip *.ear *.war *.sar *.apk *.nupkg *.exe *.dll);;All files (*.*)")
        if files:
            self.file_entry.setText(",".join(files))  # Use comma instead of semicolon
            self.folder_entry.clear()  # Clear folder entry when files are selected

    def append_output(self, text):
        self.output_text.append(text)

    def clean_dependency_check_folder(self, extract_path):
        if os.path.exists(extract_path):
            for item in os.listdir(extract_path):
                item_path = os.path.join(extract_path, item)
                if item != "data":  # Preserve the 'data' folder
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                    else:
                        os.remove(item_path)

    def set_nvd_api_key(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Set NVD API Key")
        dialog.resize(300, 100)  # <-- Added line to increase dialog size
        layout = QtWidgets.QVBoxLayout(dialog)

        label = QtWidgets.QLabel("Enter NVD API Key:")
        layout.addWidget(label)

        # Entry widget for API key
        api_key_entry = QtWidgets.QLineEdit()
        layout.addWidget(api_key_entry)

        # Load the current API key if available
        current_key = self.load_nvd_api_key()
        if current_key:
            api_key_entry.setText(current_key)

        # Buttons layout
        button_layout = QtWidgets.QHBoxLayout()
        save_button = QtWidgets.QPushButton("Save")
        cancel_button = QtWidgets.QPushButton("Cancel")

        save_button.clicked.connect(lambda: self.save_nvd_api_key(api_key_entry.text(), dialog))
        cancel_button.clicked.connect(dialog.reject)

        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        dialog.exec_()

    def save_nvd_api_key(self, key, dialog):
        if not key.strip():
            QMessageBox.warning(self, "Invalid Input", "API key cannot be empty.")
            return

        # Create XML structure for saving
        root = ET.Element("configuration")
        api_key_element = ET.SubElement(root, "nvd_api_key")
        api_key_element.text = key.strip()

        # Get the directory of the current script
        try:
            program_dir = os.path.dirname(os.path.abspath(__file__))

            # Paths for both the current directory and the _internal directory
            config_paths = [
                os.path.join(program_dir, "configuration.xml"),
                os.path.join(program_dir, "_internal", "configuration.xml")
            ]

            tree = ET.ElementTree(root)

            # Save the configuration in both locations
            for config_path in config_paths:
                try:
                    # Ensure the directory exists for the _internal path
                    os.makedirs(os.path.dirname(config_path), exist_ok=True)
                    tree.write(config_path, encoding="utf-8", xml_declaration=True)

                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to save configuration to {config_path}:\n{e}")
                    return

            QMessageBox.information(self, "Success", "NVD API Key saved in Configuration File.")
            dialog.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save configuration:\n{e}")

    def load_nvd_api_key(self):
        """Load the current NVD API Key from configuration files."""
        program_dir = os.path.dirname(os.path.abspath(__file__))

        config_paths = [
            os.path.join(program_dir, "configuration.xml"),
            os.path.join(program_dir, "_internal", "configuration.xml")
        ]

        for config_path in config_paths:
            if os.path.exists(config_path):
                try:
                    tree = ET.parse(config_path)
                    root = tree.getroot()
                    api_key_element = root.find("nvd_api_key")
                    if api_key_element is not None:
                        return api_key_element.text
                except Exception as e:
                    QMessageBox.warning(self, "Warning", f"Error reading configuration file {config_path}:\n{e}")

        return None

    def download_dependency_check(self):
        """Download and extract the latest Dependency Check version correctly with a progress bar."""
        version_url = "https://dependency-check.github.io/DependencyCheck/current.txt"

        try:
            self.append_output("Fetching latest Dependency Check version...")
            version_response = requests.get(version_url)
            if version_response.status_code == 200:
                version = version_response.text.strip()
                download_url = f"https://github.com/dependency-check/DependencyCheck/releases/download/v{version}/dependency-check-{version}-release.zip"
                save_path = "dependency-check.zip"
                extract_temp = "dependency-check-temp"
                extract_final = "dependency-check"

                self.append_output("Cleaning up existing Dependency Check folder...")
                self.clean_dependency_check_folder(extract_final)

                self.append_output(f"Downloading Dependency Check {version}...")

                # Create a progress bar
                progress_dialog = QtWidgets.QProgressDialog("Downloading Dependency Check...", "Cancel", 0, 100, self)
                progress_dialog.setWindowTitle("Downloading")
                progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
                progress_dialog.setMinimumDuration(0)
                progress_dialog.setAutoClose(True)
                progress_dialog.setAutoReset(True)

                response = requests.get(download_url, stream=True)
                if response.status_code == 200:
                    total_size = int(response.headers.get("content-length", 1))
                    downloaded_size = 0

                    with open(save_path, "wb") as file:
                        for chunk in response.iter_content(chunk_size=1024):
                            if chunk:
                                file.write(chunk)
                                downloaded_size += len(chunk)

                                # Update progress bar
                                percent = int((downloaded_size / total_size) * 100)
                                progress_dialog.setValue(percent)
                                if progress_dialog.wasCanceled():
                                    self.append_output("Download canceled.")
                                    os.remove(save_path)
                                    return

                    self.append_output("Download complete. Extracting files...")
                    with zipfile.ZipFile(save_path, "r") as zip_ref:
                        zip_ref.extractall(extract_temp)
                    os.remove(save_path)

                    # Move extracted files correctly
                    extracted_main_folder = os.path.join(extract_temp, "dependency-check")
                    if os.path.exists(extracted_main_folder):
                        for item in os.listdir(extracted_main_folder):
                            shutil.move(os.path.join(extracted_main_folder, item), extract_final)
                        shutil.rmtree(extract_temp)  # Clean up the temp folder

                    self.append_output("Dependency Check is ready to use.")
                else:
                    self.append_output("Failed to download Dependency Check.")
            else:
                self.append_output("Failed to fetch the latest version.")
        except Exception as e:
            self.append_output(f"Error: {str(e)}")

    def start_scan(self):
        source_path = self.folder_entry.text().strip()
        files = self.file_entry.text().strip().split(",")  # Split by semicolon
        project_name = self.project_entry.text().strip()
        report_format = self.format_dropdown.currentText().upper()
        dep_check_path = os.path.abspath(os.path.join("dependency-check", "bin", "dependency-check.bat"))

        if not project_name or (not source_path and not any(files)):
            QtWidgets.QMessageBox.warning(self, "Invalid Input", "Please enter a valid project name and scan path.")
            return

        if not os.path.exists(dep_check_path):
            reply = QtWidgets.QMessageBox.question(
                self, "Error", "Dependency Check not found. Download now?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
            if reply == QtWidgets.QMessageBox.Yes:
                self.download_dependency_check()
            return

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"{project_name}_{timestamp}.{report_format.lower()}"
        output_file_path = os.path.abspath(os.path.join("Reports", report_filename))
        log_file_path = os.path.abspath(os.path.join("Logs", f"{project_name}_{timestamp}.log"))

        # Prepare scan paths
        scan_paths = []
        if source_path:
            scan_paths.append(os.path.abspath(source_path))
        if files:
            scan_paths.extend(os.path.abspath(file) for file in files if file)

        # Build the command
        command = [dep_check_path, "--project", project_name]

        for path in scan_paths:
            command += ["--scan", path]

        command += ["--out", output_file_path, "--format", report_format]

        # Load API key if available
        config_paths = [
            os.path.abspath("configuration.xml"),
            os.path.abspath(os.path.join("_internal", "configuration.xml"))
        ]

        api_key = None
        for config_path in config_paths:
            if os.path.exists(config_path):
                try:
                    tree = ET.parse(config_path)
                    root = tree.getroot()
                    api_key = root.findtext("nvd_api_key")
                    break  # Exit the loop once we find the API key
                except ET.ParseError:
                    self.append_output(f"Error parsing {config_path}")

        if not api_key:
            self.set_nvd_api_key()
            for config_path in config_paths:
                if os.path.exists(config_path):
                    try:
                        tree = ET.parse(config_path)
                        root = tree.getroot()
                        api_key = root.findtext("nvd_api_key")
                        break  # Exit the loop once we find the API key
                    except ET.ParseError:
                        self.append_output(f"Error parsing {config_path} after setting key")

        if api_key:
            command += ["--nvdApiKey", api_key]

        def run_scan():
            self.append_output(f"Running: {' '.join(command)}")
            try:
                with open(log_file_path, "w", encoding="utf-8") as log_file:
                    log_file.write(f"Command: {' '.join(command)}\n\n")
                    process = subprocess.Popen(
                        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=True
                    )
                    for line in iter(process.stdout.readline, ''):
                        if line:
                            cleaned_line = line.strip()
                            QtCore.QMetaObject.invokeMethod(
                                self.output_text, "append", QtCore.Qt.QueuedConnection,
                                QtCore.Q_ARG(str, cleaned_line)
                            )
                            log_file.write(cleaned_line + "\n")
                    process.wait()
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                QtCore.QMetaObject.invokeMethod(
                    self.output_text, "append", QtCore.Qt.QueuedConnection,
                    QtCore.Q_ARG(str, error_msg)
                )
                with open(log_file_path, "a", encoding="utf-8") as log_file:
                    log_file.write(error_msg + "\n")
            finally:
                QtCore.QMetaObject.invokeMethod(
                    self, "scan_finished", QtCore.Qt.QueuedConnection,
                    QtCore.Q_ARG(str, output_file_path)
                )

        self.scan_button.setEnabled(False)
        threading.Thread(target=run_scan, daemon=True).start()

    @QtCore.pyqtSlot(str)
    def scan_finished(self, output_file_path):
        self.scan_button.setEnabled(True)
        QtWidgets.QMessageBox.information(
            self, "Scan Complete",
            f"Scan completed successfully.\nReport saved at:\n{output_file_path}"
        )


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    gui = DependencyCheckGUI()
    # Set the main window size (width, height)
    gui.resize(800, 600)  # Example size, adjust as needed
    # Set the window icon
    app.setWindowIcon(QtGui.QIcon('assets/DC.ico'))
    gui.show()
    # Check Dependency Check version on startup
    gui.check_dctools_version_startup()
    app.exec_()
