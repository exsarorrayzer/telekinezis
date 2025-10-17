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
    def show_banner(self):
        banner = f"""
    {Fore.BLUE}╔══════════════════════════════════════════════╗
    ║               {Fore.YELLOW}TELEKINEZIS{Fore.BLUE}                 ║
    ║           {Fore.GREEN}Complete File Protection{Fore.BLUE}          ║
    ╚══════════════════════════════════════════════╝{Style.RESET_ALL}
        """
        print(banner)

    def start(self):
        while True:
            self.show_menu()
            choice = input(f"{Fore.CYAN}Select option: {Style.RESET_ALL}")
            
            if choice == "1":
                self.quick_backup()
            elif choice == "2":
                self.advanced_backup()
            elif choice == "3":
                self.upload_to_0x0()
            elif choice == "4":
                self.backup_status()
            elif choice == "5":
                self.scheduled_backup()
            elif choice == "6":
                print(f"{Fore.GREEN}Exiting Telekinezis Backup System...{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}Invalid option!{Style.RESET_ALL}")

    def show_menu(self):
        print(f"\n{Fore.YELLOW}{'='*50}")
        print("BACKUP MENU")
        print(f"{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1. Quick Backup (Single ZIP)")
        print(f"{Fore.BLUE}2. Advanced Backup (Multiple Options)")
        print(f"{Fore.MAGENTA}3. Upload to 0x0.st")
        print(f"{Fore.CYAN}4. Backup Status & Info")
        print(f"{Fore.YELLOW}5. Scheduled Backup")
        print(f"{Fore.RED}6. Exit{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'='*50}{Style.RESET_ALL}")

    def quick_backup(self):
        print(f"\n{Fore.GREEN}🚀 Quick Backup System{Style.RESET_ALL}")
        password = getpass.getpass(f"{Fore.CYAN}Set password (leave empty for no password): {Style.RESET_ALL}")
        filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        
        result = self.create_zip_backup('.', filename, password if password else None)
        if result:
            print(f"{Fore.GREEN}✅ Backup created: {filename}{Style.RESET_ALL}")
            self.show_backup_info(filename)
        else:
            print(f"{Fore.RED}❌ Backup failed!{Style.RESET_ALL}")

    def advanced_backup(self):
        print(f"\n{Fore.BLUE}🔧 Advanced Backup Options:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1. Separate ZIPS for different file types")
        print(f"{Fore.BLUE}2. Hidden name ZIP")
        print(f"{Fore.MAGENTA}3. Password protected ZIP")
        print(f"{Fore.CYAN}4. All in one ZIP")
        print(f"{Fore.YELLOW}5. Compressed with progress bar")
        
        option = input(f"{Fore.CYAN}Select backup type: {Style.RESET_ALL}")
        
        if option == "1":
            self.separate_zips_backup()
        elif option == "2":
            self.hidden_name_backup()
        elif option == "3":
            self.password_backup()
        elif option == "4":
            self.complete_backup()
        elif option == "5":
            self.compressed_with_progress()

    def separate_zips_backup(self):
        print(f"\n{Fore.GREEN}📁 Creating separate ZIPS by file type...{Style.RESET_ALL}")
        file_types = {
            'text': ['.txt', '.md', '.log', '.doc', '.docx'],
            'code': ['.py', '.js', '.html', '.css', '.php', '.java', '.cpp'],
            'media': ['.jpg', '.png', '.jpeg', '.gif', '.mp4', '.mp3', '.avi'],
            'data': ['.json', '.xml', '.csv', '.sql', '.db'],
            'archives': ['.zip', '.rar', '.tar', '.gz']
        }
        
        for category, extensions in file_types.items():
            files = self.get_files_by_extensions(extensions)
            if files:
                filename = f"{category}_backup_{datetime.now().strftime('%H%M%S')}.zip"
                self.create_zip_from_files(files, filename)
                print(f"{Fore.GREEN}✅ Created {category} backup: {filename}{Style.RESET_ALL}")

    def hidden_name_backup(self):
        import random
        import string
        
        print(f"\n{Fore.BLUE}🕵️ Creating hidden backup...{Style.RESET_ALL}")
        hidden_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15)) + ".zip"
        password = getpass.getpass(f"{Fore.CYAN}Set password for hidden ZIP: {Style.RESET_ALL}")
        result = self.create_zip_backup('.', hidden_name, password)
        if result:
            print(f"{Fore.GREEN}✅ Hidden backup created: {hidden_name}{Style.RESET_ALL}")

    def password_backup(self):
        print(f"\n{Fore.MAGENTA}🔐 Creating password protected backup...{Style.RESET_ALL}")
        password = getpass.getpass(f"{Fore.CYAN}Set strong password: {Style.RESET_ALL}")
        if len(password) < 4:
            print(f"{Fore.RED}❌ Password too weak!{Style.RESET_ALL}")
            return
            
        filename = f"secure_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        result = self.create_zip_backup('.', filename, password)
        if result:
            print(f"{Fore.GREEN}✅ Password protected backup created: {filename}{Style.RESET_ALL}")

    def complete_backup(self):
        print(f"\n{Fore.CYAN}📦 Creating complete system backup...{Style.RESET_ALL}")
        password = getpass.getpass(f"{Fore.CYAN}Set master password (leave empty for no password): {Style.RESET_ALL}")
        filename = f"complete_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        result = self.create_zip_backup('.', filename, password if password else None)
        if result:
            print(f"{Fore.GREEN}✅ Complete backup created: {filename}{Style.RESET_ALL}")

    def compressed_with_progress(self):
        print(f"\n{Fore.YELLOW}📊 Creating compressed backup with progress...{Style.RESET_ALL}")
        filename = f"progress_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        result = self.create_zip_with_progress('.', filename)
        if result:
            print(f"{Fore.GREEN}✅ Progress backup created: {filename}{Style.RESET_ALL}")

    def create_zip_with_progress(self, source_dir, zip_name):
        try:
            all_files = []
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    if file != zip_name and not file.startswith('.'):
                        file_path = os.path.join(root, file)
                        all_files.append(file_path)
            
            with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in tqdm(all_files, desc=f"{Fore.CYAN}Compressing", unit="file"):
                    arcname = os.path.relpath(file_path, source_dir)
                    zipf.write(file_path, arcname)
            return True
        except Exception as e:
            print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
            return False

    def create_zip_backup(self, source_dir, zip_name, password=None):
        try:
            with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(source_dir):
                    for file in files:
                        if file != zip_name and not file.startswith('.'):
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, source_dir)
                            zipf.write(file_path, arcname)
                
                if password:
                    zipf.setpassword(password.encode())
            return True
        except Exception as e:
            print(f"{Fore.RED}❌ Backup error: {e}{Style.RESET_ALL}")
            return False

    def create_zip_from_files(self, file_list, zip_name):
        try:
            with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in file_list:
                    if os.path.exists(file_path):
                        zipf.write(file_path, os.path.basename(file_path))
            return True
        except Exception as e:
            print(f"{Fore.RED}❌ Error creating ZIP: {e}{Style.RESET_ALL}")
            return False

    def get_files_by_extensions(self, extensions):
        matching_files = []
        for root, dirs, files in os.walk('.'):
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    matching_files.append(os.path.join(root, file))
        return matching_files

    def upload_to_0x0(self):
        print(f"\n{Fore.MAGENTA}☁️  Upload to 0x0.st{Style.RESET_ALL}")
        zip_files = [f for f in os.listdir('.') if f.endswith('.zip')]
        
        if not zip_files:
            print(f"{Fore.RED}❌ No ZIP files found!{Style.RESET_ALL}")
            return
            
        for i, zip_file in enumerate(zip_files):
            print(f"{Fore.CYAN}{i+1}. {zip_file}{Style.RESET_ALL}")
        
        try:
            choice = int(input(f"{Fore.CYAN}Select ZIP to upload: {Style.RESET_ALL}")) - 1
            if 0 <= choice < len(zip_files):
                file_to_upload = zip_files[choice]
                print(f"{Fore.YELLOW}📤 Uploading {file_to_upload}...{Style.RESET_ALL}")
                
                with open(file_to_upload, 'rb') as f:
                    response = requests.post('https://0x0.st', files={'file': f})
                    if response.status_code == 200:
                        print(f"{Fore.GREEN}✅ Upload successful: {response.text}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}❌ Upload failed! Status: {response.status_code}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Invalid selection!{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}❌ Upload error: {e}{Style.RESET_ALL}")

    def backup_status(self):
        print(f"\n{Fore.CYAN}📊 Backup Status & Information{Style.RESET_ALL}")
        zip_files = [f for f in os.listdir('.') if f.endswith('.zip')]
        
        if not zip_files:
            print(f"{Fore.YELLOW}⚠️  No backup files found{Style.RESET_ALL}")
            return
            
        total_size = 0
        print(f"\n{Fore.GREEN}Found {len(zip_files)} backup files:{Style.RESET_ALL}")
        
        for zip_file in zip_files:
            size = os.path.getsize(zip_file)
            total_size += size
            created = datetime.fromtimestamp(os.path.getctime(zip_file))
            print(f"{Fore.CYAN}📁 {zip_file}")
            print(f"   Size: {self.format_size(size)}")
            print(f"   Created: {created.strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
            
        print(f"\n{Fore.YELLOW}Total backup size: {self.format_size(total_size)}{Style.RESET_ALL}")

    def scheduled_backup(self):
        print(f"\n{Fore.YELLOW}⏰ Scheduled Backup{Style.RESET_ALL}")
        print(f"{Fore.CYAN}This feature would run backups automatically")
        print(f"at specified intervals (daily, weekly, monthly){Style.RESET_ALL}")
        print(f"{Fore.GREEN}Feature coming in next version...{Style.RESET_ALL}")

    def format_size(self, size_bytes):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"

    def show_backup_info(self, filename):
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"{Fore.CYAN}📋 Backup Info:")
            print(f"   File: {filename}")
            print(f"   Size: {self.format_size(size)}")
            print(f"   MD5: {self.get_file_hash(filename)}{Style.RESET_ALL}")

    def get_file_hash(self, filename):
        try:
            hasher = hashlib.md5()
            with open(filename, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except:
            return "Unknown"