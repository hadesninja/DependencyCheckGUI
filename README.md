# Dependency Check GUI

**DependencyCheckGUI** is a graphical user interface (GUI) for running **OWASP Dependency-Check** command-line tools.  
It simplifies vulnerability scanning of software dependencies with an easy-to-use interface, additional CVE tools, and report management features.  

> ⚡ Built with **Python (PyQt5)** for a modern and optimized experience.  

---

## ✨ Features

### 🛠 Dependency Check Integration
- 📥 Download and install the latest or specific versions of Dependency-Check.  
- 🔄 Check the installed version of Dependency-Check.  
- 🗑 Purge outdated **NVD (National Vulnerability Database)** data.  

### ⚙️ Preferences
- 🔑 **Set NVD API Key** directly in the app for faster and more reliable CVE lookups.  

### 📂 Folder & File Selection
- 📁 **Browse Folder**: Scan entire project folders.  
- 📄 **Browse Files**: Select individual files (`.jar`, `.exe`, `.zip`, etc.).  

### 📑 Custom Reports
- 🏷 Define a **project name** for reports and logs.  
- 📊 Automatically organizes report filenames based on project name.  

### 🚀 Scan Execution
- ▶️ Run scans on selected files/folders.  
- 📜 Real-time logs shown in a scrollable text field.  
- 🔑 API key support for enhanced NVD data retrieval.  

### 🧰 Tools Menu Enhancements
- 📝 **CVE Details**: Enter single or multiple CVE IDs (comma-separated) to fetch details.  
- ☕ **Jar Vulnerability Finder**: Select a JAR file and fetch reported CVEs.  

### 📦 Downloads & Updates
- ⬇️ Automatically download the latest Dependency-Check.  
- 📊 Progress bar for downloads and extraction.  

---

## 🖥️ Menu Structure

The GUI now contains **three main menus**:  

### 📂 File
- 📑 Open Reports Folder  
- 📑 Open Logs Folder  
- 🔑 Preferences → Set NVD API Key  
- 🗑 Options → Purge NVD Data  
- ❌ Exit  

### 🧰 Tools
- 📝 CVE Details  
- ☕ Jar Vulnerability Finder  

### ❓ Help
- 🔎 Check Version of DC Tools  
- ⬆️ Update DC Tools to Latest Version  
- ℹ️ About  

---

## 🚀 Usage

### ▶️ Run from Executable
- 📦 **Windows Installer (Recommended):**  
  Download the installer from the **Releases** section.  
  Run the installer to set up the application. *(No administrator rights required).*  

- ⚡ **Portable Executable:**  
  - **Before v1.2:** A single `.exe` portable file was provided that could be run directly.  
  - **Since v1.2:** The portable release is distributed as a `.zip` archive.  
    Extract the archive and run the included `.exe` file to launch the application.
     

### ▶️ Run from Source
```bash
git clone https://github.com/your-username/DependencyCheckGUI.git
cd DependencyCheckGUI
pip install -r requirements.txt
python DependencyCheckGUI.py
```

---

## ⚡ How It Works
- 🧩 Uses OWASP Dependency-Check (`dependency-check.bat`) to perform scans.  
- 📥 Downloads and updates Dependency-Check automatically if missing.  
- 🔑 Stores and uses your NVD API key for faster, reliable results.  
- ☕ Includes a JAR CVE Finder and CVE ID Lookup tools.  

---

## 📋 Requirements

- ☕ **Java 11+**  
- 🌐 Internet access for Dependency-Check and CVE data  

### 📦 Python Dependencies
- `pyqt5`  
- `requests`  
- `subprocess`  
- `shutil`, `os`  
- `zipfile`  
- `threading`  

Install all with:
```bash
pip install -r requirements.txt
```

---

## 🛠 Troubleshooting
- ❌ **Dependency-Check not found** → Program will prompt to download.  
- 🔑 **NVD API issues** → Ensure valid API key is set in Preferences.  
- 🌐 **Network errors** → Verify internet connectivity.  
- 🗑 **No NVD data to purge** → Tool will notify if purge isn’t needed.  

---

## 📜 License
Licensed under the **MIT License**. See the [LICENSE](LICENSE) file.  

---

## 🙌 Acknowledgements
 
- **PyQt5** – GUI Framework  
- **Requests** – For downloads & API calls  
- **GitHub API** – To fetch DC versions  
- **Python** – Cross-platform base
- **[OWASP Dependency-Check](https://owasp.org/www-project-dependency-check/)** – For scanning dependencies for known vulnerabilities.  
- **[Solr Search API](https://solr.apache.org/)** – For indexing and searching project or CVE data.  
- **[NVD API (National Vulnerability Database)](https://nvd.nist.gov/developers)** – To fetch detailed CVE information for dependencies.  

We appreciate the work of these open-source communities for providing invaluable tools and data.

---

✨ *A simple yet powerful GUI to supercharge your OWASP Dependency-Check workflows!* 🚀
