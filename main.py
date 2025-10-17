from colorama import Fore, Style, init
from modules.backup_manager import BackupManager

init(autoreset=True)

def show_banner():
    banner = f"""
    {Fore.CYAN}╔══════════════════════════════════════════════╗
    ║            {Fore.YELLOW}TELEKINEZIS BACKUP SYSTEM{Fore.CYAN}         ║
    ║           {Fore.GREEN}${Fore.CYAN}                                 ║
    ║                                             ║
    ║              {Fore.YELLOW}Author: exsarorrayzer{Fore.CYAN}          ║
    ║                 {Fore.YELLOW}Version: 2.1{Fore.CYAN}                ║
    ╚══════════════════════════════════════════════╝{Style.RESET_ALL}
    """
    print(banner)

def main():
    show_banner()
    backup_manager = BackupManager()
    backup_manager.start()

if __name__ == "__main__":
    main()