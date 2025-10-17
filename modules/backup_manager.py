import os
import zipfile
import getpass
import time
import hashlib
from datetime import datetime
from colorama import Fore, Style, init
import requests
from tqdm import tqdm

init(autoreset=True)

class BackupManager:
    def __init__(self):
        self.backup_path = None

    def show_banner(self):
        banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════╗
║              {Fore.MAGENTA}TELEKINEZIS BACKUP{Fore.CYAN}              ║
║             {Fore.YELLOW}Advanced Backup System{Fore.CYAN}            ║
║                                              ║
║              {Fore.GREEN}Author: exsarorrayzer{Fore.CYAN}             ║
║                 {Fore.WHITE}Version: 2.1{Fore.CYAN}                  ║
╚══════════════════════════════════════════════╝{Style.RESET_ALL}
        """
        print(banner)

    def start(self):
        self.set_backup_path()
        while True:
            self.show_menu()
            choice = input(f"{Fore.YELLOW}Select option: {Style.RESET_ALL}")
            
            if choice == "1":
                self.quick_backup()
            elif choice == "2":
                self.advanced_backup()
            elif choice == "3":
                self.upload_to_0x0()
            elif choice == "4":
                self.backup_status()
            elif choice == "5":
                print(f"{Fore.GREEN}Exiting...{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}Invalid option!{Style.RESET_ALL}")

    def set_backup_path(self):
        print(f"\n{Fore.CYAN}Current directory: {os.getcwd()}{Style.RESET_ALL}")
        change = input(f"{Fore.YELLOW}Change backup path? (y/n): {Style.RESET_ALL}").lower()
        if change == 'y':
            new_path = input(f"{Fore.YELLOW}Enter path: {Style.RESET_ALL}")
            if os.path.exists(new_path):
                os.chdir(new_path)
                print(f"{Fore.GREEN}Path changed to: {os.getcwd()}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Path not found! Using current directory.{Style.RESET_ALL}")
        
        self.backup_path = os.getcwd()

    def show_menu(self):
        print(f"\n{Fore.CYAN}{'='*50}")
        print(f"{Fore.MAGENTA}BACKUP MENU")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1. Quick Backup")
        print(f"{Fore.BLUE}2. Advanced Backup")
        print(f"{Fore.YELLOW}3. Upload to 0x0.st")
        print(f"{Fore.CYAN}4. Backup Status")
        print(f"{Fore.RED}5. Exit{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")

    def quick_backup(self):
        print(f"\n{Fore.GREEN}Quick Backup{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Backup path: {self.backup_path}{Style.RESET_ALL}")
        
        filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        result = self.create_zip_backup(self.backup_path, filename)
        
        if result:
            print(f"{Fore.GREEN}Backup created: {filename}{Style.RESET_ALL}")
            self.ask_backup_options(filename)

    def advanced_backup(self):
        print(f"\n{Fore.BLUE}Advanced Backup Options{Style.RESET_ALL}")
        print(f"{Fore.CYAN}1. All in One Backup")
        print(f"{Fore.CYAN}2. Separate by File Types{Style.RESET_ALL}")
        
        option = input(f"{Fore.YELLOW}Select backup type: {Style.RESET_ALL}")
        
        if option == "1":
            self.all_in_one_backup()
        elif option == "2":
            self.separate_zips_backup()

    def all_in_one_backup(self):
        print(f"\n{Fore.GREEN}Creating All in One Backup...{Style.RESET_ALL}")
        
        filename = f"all_in_one_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        result = self.create_zip_backup(self.backup_path, filename)
        
        if result:
            print(f"{Fore.GREEN}All in One backup created: {filename}{Style.RESET_ALL}")
            self.ask_backup_options(filename)

    def separate_zips_backup(self):
        print(f"\n{Fore.GREEN}Creating separate ZIPS by file type...{Style.RESET_ALL}")
        
        file_types = {
            'text': ['.txt', '.md', '.log', '.doc', '.docx', '.pdf', '.rtf'],
            'code': ['.py', '.js', '.html', '.css', '.php', '.java', '.cpp', '.c', '.h'],
            'media': ['.jpg', '.png', '.jpeg', '.gif', '.bmp', '.svg', '.mp4', '.mp3', '.avi', '.mkv', '.wav'],
            'data': ['.json', '.xml', '.csv', '.sql', '.db', '.xlsx', '.xls'],
            'archives': ['.zip', '.rar', '.tar', '.gz', '.7z', '.iso'],
            'executables': ['.apk', '.exe', '.deb', '.rpm', '.msi']
        }
        
        all_files_in_backup = set()
        created_files = []
        
        # Known file types
        for category, extensions in file_types.items():
            files = self.get_files_by_extensions(extensions)
            if files:
                filename = f"{category}_{datetime.now().strftime('%H%M%S')}.zip"
                if self.create_zip_from_files(files, filename):
                    print(f"{Fore.GREEN}Created {category} backup: {filename}{Style.RESET_ALL}")
                    created_files.append(filename)
                    all_files_in_backup.update(files)
        
        # Unknown file types
        all_files = set()
        for root, dirs, files in os.walk(self.backup_path):
            for file in files:
                if not file.endswith('.zip'):
                    file_path = os.path.join(root, file)
                    all_files.add(file_path)
        
        unknown_files = all_files - all_files_in_backup
        if unknown_files:
            filename = f"unknown_types_{datetime.now().strftime('%H%M%S')}.zip"
            if self.create_zip_from_files(list(unknown_files), filename):
                print(f"{Fore.GREEN}Created unknown types backup: {filename}{Style.RESET_ALL}")
                created_files.append(filename)
        
        if created_files:
            self.ask_backup_options_multiple(created_files)

    def ask_backup_options(self, filename):
        print(f"\n{Fore.YELLOW}Backup Options for {filename}{Style.RESET_ALL}")
        
        # Password protection
        password_option = input(f"{Fore.YELLOW}Add password protection? (y/n): {Style.RESET_ALL}").lower()
        if password_option == 'y':
            pwd = getpass.getpass(f"{Fore.YELLOW}Enter password: {Style.RESET_ALL}")
            if self.add_password_to_zip(filename, pwd):
                print(f"{Fore.GREEN}Password added successfully{Style.RESET_ALL}")
        
        # Anonymous name
        anon_option = input(f"{Fore.YELLOW}Use anonymous name? (y/n): {Style.RESET_ALL}").lower()
        if anon_option == 'y':
            new_name = self.generate_anonymous_name()
            os.rename(filename, new_name)
            filename = new_name
            print(f"{Fore.GREEN}Renamed to: {filename}{Style.RESET_ALL}")
        
        # Upload to 0x0
        upload_option = input(f"{Fore.YELLOW}Upload to 0x0.st? (y/n): {Style.RESET_ALL}").lower()
        if upload_option == 'y':
            self.upload_single_file(filename)

    def ask_backup_options_multiple(self, filenames):
        print(f"\n{Fore.YELLOW}Backup Options for {len(filenames)} files{Style.RESET_ALL}")
        
        # Password protection for all
        password_option = input(f"{Fore.YELLOW}Add password protection to all? (y/n): {Style.RESET_ALL}").lower()
        if password_option == 'y':
            pwd = getpass.getpass(f"{Fore.YELLOW}Enter password for all: {Style.RESET_ALL}")
            for filename in filenames:
                if self.add_password_to_zip(filename, pwd):
                    print(f"{Fore.GREEN}Password added to {filename}{Style.RESET_ALL}")
        
        # Anonymous names for all
        anon_option = input(f"{Fore.YELLOW}Use anonymous names for all? (y/n): {Style.RESET_ALL}").lower()
        if anon_option == 'y':
            new_filenames = []
            for filename in filenames:
                new_name = self.generate_anonymous_name()
                os.rename(filename, new_name)
                new_filenames.append(new_name)
                print(f"{Fore.GREEN}Renamed {filename} to {new_name}{Style.RESET_ALL}")
            filenames = new_filenames
        
        # Upload all to 0x0
        upload_option = input(f"{Fore.YELLOW}Upload all to 0x0.st? (y/n): {Style.RESET_ALL}").lower()
        if upload_option == 'y':
            self.upload_multiple_files(filenames)

    def create_zip_backup(self, source_dir, zip_name, password=None):
        try:
            all_files = []
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    if not file.endswith('.zip'):
                        file_path = os.path.join(root, file)
                        all_files.append(file_path)
            
            with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in tqdm(all_files, desc=f"{Fore.CYAN}Compressing", unit="file", colour='green'):
                    try:
                        arcname = os.path.relpath(file_path, source_dir)
                        zipf.write(file_path, arcname)
                    except Exception as e:
                        continue
            
            if password:
                self.add_password_to_zip(zip_name, password)
                
            return True
        except Exception as e:
            print(f"{Fore.RED}Backup error: {e}{Style.RESET_ALL}")
            return False

    def create_zip_from_files(self, file_list, zip_name, password=None):
        try:
            with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in tqdm(file_list, desc=f"{Fore.CYAN}Compressing", unit="file", colour='blue'):
                    try:
                        if os.path.exists(file_path):
                            zipf.write(file_path, os.path.basename(file_path))
                    except Exception as e:
                        continue
            
            if password:
                self.add_password_to_zip(zip_name, password)
                
            return True
        except Exception as e:
            print(f"{Fore.RED}Error creating ZIP: {e}{Style.RESET_ALL}")
            return False

    def add_password_to_zip(self, zip_name, password):
        try:
            # Create temporary zip with password
            temp_name = f"temp_{zip_name}"
            with zipfile.ZipFile(zip_name, 'r') as zip_read:
                with zipfile.ZipFile(temp_name, 'w', zipfile.ZIP_DEFLATED) as zip_write:
                    for item in zip_read.infolist():
                        data = zip_read.read(item.filename)
                        zip_write.writestr(item, data)
                    zip_write.setpassword(password.encode())
            
            os.replace(temp_name, zip_name)
            return True
        except Exception as e:
            print(f"{Fore.RED}Password error: {e}{Style.RESET_ALL}")
            return False

    def get_files_by_extensions(self, extensions):
        matching_files = []
        for root, dirs, files in os.walk(self.backup_path):
            for file in files:
                if any(file.lower().endswith(ext.lower()) for ext in extensions):
                    file_path = os.path.join(root, file)
                    matching_files.append(file_path)
        return matching_files

    def generate_anonymous_name(self):
        import random
        import string
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=12)) + ".zip"

    def upload_single_file(self, filename):
        print(f"{Fore.YELLOW}Uploading {filename} to 0x0.st...{Style.RESET_ALL}")
        try:
            with open(filename, 'rb') as f:
                response = requests.post('https://0x0.st', files={'file': f})
                if response.status_code == 200:
                    print(f"{Fore.GREEN}Upload successful: {response.text.strip()}{Style.RESET_ALL}")
                    return response.text.strip()
                else:
                    print(f"{Fore.RED}Upload failed! Status: {response.status_code}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Upload error: {e}{Style.RESET_ALL}")

    def upload_multiple_files(self, filenames):
        print(f"{Fore.YELLOW}Uploading {len(filenames)} files to 0x0.st...{Style.RESET_ALL}")
        for filename in filenames:
            self.upload_single_file(filename)

    def upload_to_0x0(self):
        print(f"\n{Fore.MAGENTA}Upload to 0x0.st{Style.RESET_ALL}")
        zip_files = [f for f in os.listdir('.') if f.endswith('.zip')]
        
        if not zip_files:
            print(f"{Fore.RED}No ZIP files found!{Style.RESET_ALL}")
            return
            
        for i, zip_file in enumerate(zip_files):
            print(f"{Fore.CYAN}{i+1}. {zip_file}{Style.RESET_ALL}")
        
        try:
            choice = int(input(f"{Fore.YELLOW}Select ZIP to upload: {Style.RESET_ALL}")) - 1
            if 0 <= choice < len(zip_files):
                file_to_upload = zip_files[choice]
                self.upload_single_file(file_to_upload)
            else:
                print(f"{Fore.RED}Invalid selection!{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Upload error: {e}{Style.RESET_ALL}")

    def backup_status(self):
        print(f"\n{Fore.CYAN}Backup Status & Information{Style.RESET_ALL}")
        zip_files = [f for f in os.listdir('.') if f.endswith('.zip')]
        
        if not zip_files:
            print(f"{Fore.YELLOW}No backup files found{Style.RESET_ALL}")
            return
            
        total_size = 0
        print(f"\n{Fore.GREEN}Found {len(zip_files)} backup files:{Style.RESET_ALL}")
        
        for zip_file in zip_files:
            size = os.path.getsize(zip_file)
            total_size += size
            created = datetime.fromtimestamp(os.path.getctime(zip_file))
            print(f"{Fore.CYAN}File: {zip_file}")
            print(f"Size: {self.format_size(size)}")
            print(f"Created: {created.strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
            print()
            
        print(f"{Fore.YELLOW}Total backup size: {self.format_size(total_size)}{Style.RESET_ALL}")

    def format_size(self, size_bytes):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"