Initial Release Changes:

- Folder Creation: Added the ensure_folders function to check and create reports and logs folders.
- Report and Log Storage: Updated the run_command function to store the report in the reports folder and logs in the logs folder.
- Dynamic Log Filename: Log filename now includes the report's filename and a timestamp (e.g., output_20231221_123456.log).
- Timestamp Generation: Utilized datetime.now().strftime to format the timestamp for the log file.
- Improved File Path Management: Used os.path.join to construct paths for report and log files more cleanly.
- Enhanced User Feedback: Added success and error messages with detailed paths to generated files.
- Validation for Mandatory Fields: Added checks to ensure both the Report Title (project_entry) and Output Report Filename (output_filename) fields are not empty.
- Display a warning message if either field is empty.
- Error Messages: The user is prompted to fill the mandatory fields with descriptive error messages.
- Mandatory Fields Implementation: Ensures smoother validation before proceeding to execute the command.
