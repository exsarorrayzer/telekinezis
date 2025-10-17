import os
import requests
from colorama import Fore, Style

class UploadManager:
    def __init__(self):
        self.services = {
            '1': {'name': '0x0.st', 'function': self.upload_0x0},
            '2': {'name': 'catbox.moe', 'function': self.upload_catbox}
        }

    def show_upload_menu(self):
        print(f"\n{Fore.CYAN}{'='*40}")
        print(f"{Fore.YELLOW}UPLOAD SERVICES")
        print(f"{Fore.CYAN}{'='*40}{Style.RESET_ALL}")
        for key, service in self.services.items():
            print(f"{Fore.GREEN}{key}. {service['name']}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*40}{Style.RESET_ALL}")

    def upload_0x0(self, file_path):
        """Upload file to 0x0.st"""
        try:
            print(f"{Fore.YELLOW}Uploading to 0x0.st...{Style.RESET_ALL}")
            cmd = f"curl -s -F 'file=@\"{file_path}\"' https://0x0.st"
            result = os.popen(cmd).read().strip()
            
            if result.startswith("http"):
                print(f"{Fore.GREEN}0x0.st Success: {result}{Style.RESET_ALL}")
                return result
            else:
                print(f"{Fore.RED}0x0.st Error: {result}{Style.RESET_ALL}")
                return None
                
        except Exception as e:
            print(f"{Fore.RED}0x0.st Upload Failed: {str(e)}{Style.RESET_ALL}")
            return None

    def upload_catbox(self, file_path):
        """Upload file to catbox.moe"""
        try:
            print(f"{Fore.YELLOW}Uploading to catbox.moe...{Style.RESET_ALL}")
            cmd = f"curl -s -F 'reqtype=fileupload' -F 'userhash=' -F 'fileToUpload=@\"{file_path}\"' https://catbox.moe/user/api.php"
            result = os.popen(cmd).read().strip()
            
            if result.startswith("http"):
                print(f"{Fore.GREEN}catbox.moe Success: {result}{Style.RESET_ALL}")
                return result
            else:
                print(f"{Fore.RED}catbox.moe Error: {result}{Style.RESET_ALL}")
                return None
                
        except Exception as e:
            print(f"{Fore.RED}catbox.moe Upload Failed: {str(e)}{Style.RESET_ALL}")
            return None

    def upload_file(self, file_path, service_choice=None):
        """Upload file to selected service"""
        if not os.path.exists(file_path):
            print(f"{Fore.RED}File not found: {file_path}{Style.RESET_ALL}")
            return None

        if service_choice is None:
            self.show_upload_menu()
            service_choice = input(f"{Fore.YELLOW}Select upload service: {Style.RESET_ALL}")

        if service_choice in self.services:
            service = self.services[service_choice]
            print(f"{Fore.CYAN}Using {service['name']}...{Style.RESET_ALL}")
            return service['function'](file_path)
        else:
            print(f"{Fore.RED}Invalid service selection!{Style.RESET_ALL}")
            return None

    def upload_multiple_files(self, file_paths, service_choice=None):
        """Upload multiple files to selected service"""
        results = {}
        
        if service_choice is None:
            self.show_upload_menu()
            service_choice = input(f"{Fore.YELLOW}Select upload service for all files: {Style.RESET_ALL}")

        for file_path in file_paths:
            if os.path.exists(file_path):
                print(f"\n{Fore.CYAN}Uploading: {os.path.basename(file_path)}{Style.RESET_ALL}")
                result = self.upload_file(file_path, service_choice)
                results[file_path] = result
            else:
                print(f"{Fore.RED}File not found: {file_path}{Style.RESET_ALL}")
                results[file_path] = None

        return results

    def get_available_services(self):
        """Return list of available upload services"""
        return [(key, service['name']) for key, service in self.services.items()]