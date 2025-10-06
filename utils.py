import sys
from colorama import Fore, Style, init as _init_colorama
_init_colorama()

def info(msg: str):
    print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} {msg}")

def success(msg: str):
    print(f"{Fore.GREEN}[OK]{Style.RESET_ALL} {msg}")

def warn(msg: str):
    print(f"{Fore.YELLOW}[WARN]{Style.RESET_ALL} {msg}")

def error(msg: str):
    print(f"{Fore.RED}[ERR]{Style.RESET_ALL} {msg}")

def action_added(msg: str):
    print(f"{Fore.GREEN}+ ADDED:{Style.RESET_ALL} {msg}")

def action_updated(msg: str):
    print(f"{Fore.BLUE}~ UPDATED:{Style.RESET_ALL} {msg}")

def action_deleted(msg: str):
    print(f"{Fore.RED}- DELETED:{Style.RESET_ALL} {msg}")
