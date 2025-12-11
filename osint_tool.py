#!/usr/bin/env python3
"""
XTrace v3.0 - Advanced OSINT Intelligence Platform
Enhanced version dengan akurasi tinggi dan fitur lengkap
Untuk penggunaan legal dan etis saja
"""

import sys
import os
from datetime import datetime
import time

# Cek dependencies
try:
    from PIL import Image
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

try:
    import dns.resolver
    DNS_AVAILABLE = True
except ImportError:
    DNS_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

from modules.colors import Colors
from modules.username import check_username
from modules.email import check_email
from modules.domain import check_domain
from modules.phone import check_phone
from modules.ip import check_ip
from modules.photo import check_photo
from modules.utils import ensure_directories, log

class XTraceOSINT:
    def __init__(self):
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        ensure_directories()
    
    def banner(self):
        """Banner aplikasi enhanced"""
        banner = f"""
{Colors.CYAN}╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║  {Colors.BOLD}██╗  ██╗████████╗██████╗  █████╗  ██████╗███████╗{Colors.END}{Colors.CYAN}            ║
║  {Colors.BOLD}╚██╗██╔╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██╔════╝{Colors.END}{Colors.CYAN}            ║
║  {Colors.BOLD} ╚███╔╝    ██║   ██████╔╝███████║██║     █████╗{Colors.END}{Colors.CYAN}              ║
║  {Colors.BOLD} ██╔██╗    ██║   ██╔══██╗██╔══██║██║     ██╔══╝{Colors.END}{Colors.CYAN}              ║
║  {Colors.BOLD}██╔╝ ██╗   ██║   ██║  ██║██║  ██║╚██████╗███████╗{Colors.END}{Colors.CYAN}            ║
║  {Colors.BOLD}╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚══════╝{Colors.END}{Colors.CYAN}            ║
║                                                               ║
║            {Colors.YELLOW}Advanced OSINT Intelligence Platform v3.0{Colors.END}{Colors.CYAN}          ║
║                  {Colors.GREEN}Enhanced & Optimized Edition{Colors.END}{Colors.CYAN}                 ║
║                                                               ║
║  {Colors.WHITE}Features: Username • Email • Domain • IP • Phone • Photo{Colors.END}{Colors.CYAN}     ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}

{Colors.YELLOW}[!] LEGAL USE ONLY - For authorized security research
[!] Session ID: {self.session_id}
[!] Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}{Colors.END}
"""
        print(banner)
        log(f"XTrace v3.0 started - Session: {self.session_id}")

    def interactive_mode(self):
        """Enhanced interactive mode"""
        while True:
            print(f"\n{Colors.BOLD}{'='*70}")
            print(f"{Colors.CYAN}╔════════════════════════════════════════════════════════════════╗")
            print(f"║           XTRACE v3.0 - MAIN MENU                              ║")
            print(f"╚════════════════════════════════════════════════════════════════╝{Colors.END}")
            print(f"{'='*70}{Colors.END}\n")
            
            print(f"{Colors.GREEN}  [1]{Colors.END} Username OSINT        - Search 100+ platforms")
            print(f"{Colors.GREEN}  [2]{Colors.END} Email OSINT           - Email analysis & validation")
            print(f"{Colors.GREEN}  [3]{Colors.END} Domain OSINT          - Domain & DNS analysis")
            print(f"{Colors.GREEN}  [4]{Colors.END} Phone OSINT           - Phone number lookup")
            print(f"{Colors.GREEN}  [5]{Colors.END} IP Address OSINT      - IP info & port scan")
            print(f"{Colors.GREEN}  [6]{Colors.END} Photo OSINT           - EXIF & GPS extraction")
            print(f"{Colors.CYAN}  [7]{Colors.END} View Reports          - Browse saved reports")
            print(f"{Colors.RED}  [0]{Colors.END} Exit\n")
            
            choice = input(f"{Colors.YELLOW}Select option [0-7]: {Colors.END}").strip()
            
            if choice == '0':
                print(f"\n{Colors.CYAN}╔════════════════════════════════════════════╗")
                print(f"║  Thank you for using XTrace v3.0!          ║")
                print(f"║  Stay safe and hack ethically!             ║")
                print(f"╚════════════════════════════════════════════╝{Colors.END}\n")
                log("Session ended by user")
                break
                
            elif choice == '1':
                username = input(f"\n{Colors.YELLOW}Enter username: {Colors.END}").strip()
                if username:
                    check_username(username, self.session_id)
                    
            elif choice == '2':
                email = input(f"\n{Colors.YELLOW}Enter email: {Colors.END}").strip()
                if email:
                    check_email(email, self.session_id)
                    
            elif choice == '3':
                domain = input(f"\n{Colors.YELLOW}Enter domain: {Colors.END}").strip()
                if domain:
                    check_domain(domain, self.session_id)
                    
            elif choice == '4':
                phone = input(f"\n{Colors.YELLOW}Enter phone number: {Colors.END}").strip()
                if phone:
                    check_phone(phone, self.session_id)
                    
            elif choice == '5':
                ip = input(f"\n{Colors.YELLOW}Enter IP address: {Colors.END}").strip()
                if ip:
                    check_ip(ip, self.session_id)
                    
            elif choice == '6':
                photo = input(f"\n{Colors.YELLOW}Enter photo path: {Colors.END}").strip()
                if photo:
                    check_photo(photo, self.session_id)
                    
            elif choice == '7':
                self.view_reports()
                
            else:
                print(f"{Colors.RED}[!] Invalid option{Colors.END}")
            
            input(f"\n{Colors.YELLOW}Press ENTER to continue...{Colors.END}")
    
    def view_reports(self):
        """View saved reports"""
        print(f"\n{Colors.BOLD}[*] Saved Reports:{Colors.END}\n")
        
        result_files = sorted([f for f in os.listdir('result') if f.endswith('.json')])
        
        if not result_files:
            print(f"{Colors.YELLOW}[!] No reports found{Colors.END}")
            return
        
        for i, filename in enumerate(result_files[-10:], 1):  # Show last 10
            print(f"  {Colors.CYAN}[{i}] {filename}{Colors.END}")
        
        print(f"\n{Colors.GREEN}[✓] Total reports: {len(result_files)}{Colors.END}")
        print(f"{Colors.CYAN}[i] Location: ./result/{Colors.END}")

def main():
    """Main function"""
    tool = XTraceOSINT()
    tool.banner()
    
    print(f"\n{Colors.BOLD}[*] Checking Dependencies...{Colors.END}")
    deps = {
        'Pillow': PILLOW_AVAILABLE,
        'dnspython': DNS_AVAILABLE,
        'BeautifulSoup4': BS4_AVAILABLE
    }
    
    all_installed = True
    for dep, available in deps.items():
        status = f"{Colors.GREEN}✓ Installed{Colors.END}" if available else f"{Colors.YELLOW}✗ Not installed{Colors.END}"
        print(f"  {dep:20s}: {status}")
        if not available:
            all_installed = False

    if not all_installed:
        print(f"\n{Colors.YELLOW}[!] Some features may be limited{Colors.END}")
        print(f"{Colors.YELLOW}[!] Install all: pip install -r requirements.txt{Colors.END}")

    time.sleep(2)
    
    tool.interactive_mode()

if __name__ == "__main__":
    try:
        main()
        
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}[!] Operation cancelled by user{Colors.END}")
        print(f"{Colors.CYAN}[i] Exiting gracefully...{Colors.END}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}[!] Fatal error: {e}{Colors.END}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
