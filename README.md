Telekinezis Backup System

Telekinezis is an advanced backup solution for Termux that provides comprehensive file protection with multiple backup options and secure cloud upload capabilities.

FEATURES

· Multiple Backup Modes
  Quick single ZIP backup
  Advanced backup with separate ZIPS for different file types
  Hidden name ZIP backups
  Password protected encrypted backups
  Complete system backup in single ZIP
  Progress bar compression with detailed status

· File Type Organization
  Text files: txt, md, log, doc, docx
  Code files: py, js, html, css, php, java, cpp
  Media files: jpg, png, jpeg, gif, mp4, mp3, avi
  Data files: json, xml, csv, sql, db
  Archive files: zip, rar, tar, gz

· Security Features
  Password protection with encryption
  Hidden filename generation
  Secure cloud upload to 0x0.st

  File integrity verification
· Additional Capabilities
  Backup status and information display
  File size formatting and statistics
  Progress visualization during compression
  Color-coded interface for better user experience

INSTALLATION

1. Install Python in Termux:
   pkg install python
2. Install required dependencies:
   pip install colorama requests tqdm
3. Run the application:
   python main.py

USAGE

1. Quick Backup
   Creates a single ZIP file with optional password protection
   Includes all files in current directory and subdirectories
2. Advanced Backup
   Separate ZIPS: Creates individual backups for different file types
   Hidden Name: Generates backups with random filenames
   Password Protected: Encrypts backup with strong password
   Complete Backup: All files in one comprehensive ZIP
   Progress Backup: Visual compression progress with status bar
3. Cloud Upload
   Upload backup files to 0x0.st file sharing service
   Provides direct download links for sharing
   Supports all ZIP files created by the system
4. Backup Status
   Displays information about all backup files
   Shows file sizes, creation dates, and total storage used
   Provides MD5 hashes for file verification

FILE STRUCTURE

main.py
modules/
backup_manager.py
init.py

NOTES

· The tool does not delete original files, only creates copies

· All backups are created in current working directory

· Password protection uses ZIP encryption

· Cloud uploads are anonymous and temporary

· Hidden names use random 15-character strings

COMMANDS

Start application: python main.py
Quick backup:Select option 1
Advanced backup:Select option 2
Cloud upload:Select option 3
Backup status:Select option 4
Exit:Select option 6

COMPATIBILITY

Designed for Termux on Android
Requires Python 3.6 or higher
Internet connection required for cloud uploads
Adequate storage space for backup files
