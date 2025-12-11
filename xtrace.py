#!/usr/bin/env python3
import argparse
import sys
import os
from datetime import datetime
import time
import subprocess

import importlib.metadata
from packaging.version import parse as parse_version

def check_and_install_dependencies():
    """Checks for required packages and prompts the user to install them if they are missing."""
    try:
        # Define requirements with package name and version specifier
        requirements = {
            "beautifulsoup4": ">=4.12.0",
            "dnspython": ">=2.4.0",
            "Pillow": ">=10.0.0"
        }
        missing_packages = []

        for package, version_spec in requirements.items():
            try:
                installed_version = importlib.metadata.version(package)
                if parse_version(installed_version) < parse_version(version_spec.strip(">=")):
                    missing_packages.append(f"{package}{version_spec}")
            except importlib.metadata.PackageNotFoundError:
                missing_packages.append(f"{package}{version_spec}")

        if missing_packages:
            print(f"{Colors.YELLOW}[!] The following required packages are missing or out of date:{Colors.END}")
            for pkg in missing_packages:
                print(f"    - {pkg}")
            
            response = input(f"{Colors.YELLOW}Would you like to install them now? (y/N): {Colors.END}").strip().lower()
            if response == 'y':
                print(f"{Colors.CYAN}[*] Installing dependencies...{Colors.END}")
                try:
                    # We install the packages without the version specifier for simplicity,
                    # letting pip resolve the latest compatible version.
                    # For more complex scenarios, parsing the full specifier would be needed.
                    package_names = [pkg.split('>=')[0] for pkg in missing_packages]
                    subprocess.check_call([sys.executable, "-m", "pip", "install", *package_names])
                    print(f"{Colors.GREEN}[✓] Dependencies installed successfully.{Colors.END}")
                    # Re-check to be sure
                    for package, version_spec in requirements.items():
                        importlib.metadata.version(package) # This will raise PackageNotFoundError if not installed
                except subprocess.CalledProcessError as e:
                    print(f"{Colors.RED}[!] Error installing dependencies: {e}{Colors.END}")
                    sys.exit(1)
                except importlib.metadata.PackageNotFoundError as e:
                    print(f"{Colors.RED}[!] A dependency issue persists even after installation: {e.name}{Colors.END}")
                    print(f"{Colors.RED}[!] Please try to resolve this manually.{Colors.END}")
                    sys.exit(1)
            else:
                print(f"{Colors.RED}[!] Cannot proceed without required dependencies. Exiting.{Colors.END}")
                sys.exit(1)

    except ImportError:
        # This error is kept in case 'packaging' itself is not available, though it's a common dependency.
        print(f"{Colors.RED}[!] `importlib.metadata` or `packaging` not available in this Python version.{Colors.END}")
        print(f"{Colors.YELLOW}Please upgrade your Python environment or manually install dependencies from requirements.txt.{Colors.END}")
        sys.exit(1)


# These imports are now guaranteed by the dependency checker.
from PIL import Image
import dns.resolver
from bs4 import BeautifulSoup

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
            
            print(f"{Colors.GREEN}  [1]{Colors.END} Username OSINT        - Search 50+ platforms")
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
    check_and_install_dependencies()
    parser = argparse.ArgumentParser(description="XTrace v3.0 - Advanced OSINT Intelligence Platform", add_help=False)

    parser.add_argument('-u', '--username', help="Search for a username")
    parser.add_argument('-e', '--email', help="Analyze an email address")
    parser.add_argument('-d', '--domain', help="Analyze a domain")
    parser.add_argument('-p', '--phone', help="Analyze a phone number")
    parser.add_argument('-i', '--ip', help="Analyze an IP address")
    parser.add_argument('-ph', '--photo', help="Analyze a photo")
    parser.add_argument('-h', '--help', action='store_true', help='Show this help message and exit')

    args = parser.parse_args()

    tool = XTraceOSINT()

    if args.help:
        print_help()
        sys.exit(0)

    if len(sys.argv) == 1:
        tool.banner()
        tool.interactive_mode()
        sys.exit(0)

    session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    if args.username:
        check_username(args.username, session_id)
    elif args.email:
        check_email(args.email, session_id)
    elif args.domain:
        check_domain(args.domain, session_id)
    elif args.phone:
        check_phone(args.phone, session_id)
    elif args.ip:
        check_ip(args.ip, session_id)
    elif args.photo:
        check_photo(args.photo, session_id)
    else:
        parser.print_help()

def print_help():
    """Print help menu"""
    help_text = f"""
{Colors.CYAN}╔═══════════════════════════════════════════════════════════════╗
║                    XTRACE v3.0 - HELP MENU                    ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}

{Colors.BOLD}USAGE:{Colors.END}
  xtrace [options]

{Colors.BOLD}OPTIONS:{Colors.END}
  {Colors.GREEN}-u, --username <username>{Colors.END}    Search username across 50+ platforms
  {Colors.GREEN}-e, --email <email>{Colors.END}          Email validation and OSINT
  {Colors.GREEN}-d, --domain <domain>{Colors.END}        Domain analysis and DNS lookup
  {Colors.GREEN}-p, --phone <phone>{Colors.END}          Phone number lookup and analysis
  {Colors.GREEN}-i, --ip <ip>{Colors.END}               IP address information and port scan
  {Colors.GREEN}-ph, --photo <photo>{Colors.END}        Photo EXIF and metadata extraction
  {Colors.GREEN}-h, --help{Colors.END}                  Show this help menu

{Colors.BOLD}EXAMPLES:{Colors.END}
  {Colors.CYAN}xtrace -u john_doe{Colors.END}
  {Colors.CYAN}xtrace -e test@example.com{Colors.END}
  {Colors.CYAN}xtrace -d example.com{Colors.END}
  {Colors.CYAN}xtrace -p +6281234567890{Colors.END}
  {Colors.CYAN}xtrace -i 8.8.8.8{Colors.END}
  {Colors.CYAN}xtrace -ph image.jpg{Colors.END}

{Colors.BOLD}FEATURES:{Colors.END}
  • Username search across 50+ social media & platforms
  • Email validation, breach check, and provider detection
  • Domain DNS analysis, subdomain discovery, SSL check
  • Phone number validation and provider lookup (ID support)
  • IP geolocation, port scanning, and threat intelligence
  • Photo EXIF extraction including GPS coordinates
  • Automated report generation (JSON & HTML)
  • Multi-threaded scanning for speed
  • Comprehensive logging system

{Colors.BOLD}OUTPUT:{Colors.END}
  • Results saved in: {Colors.CYAN}./result/{Colors.END}
  • HTML reports in: {Colors.CYAN}./reports/{Colors.END}
  • Logs saved in: {Colors.CYAN}./logs/{Colors.END}

{Colors.BOLD}DEPENDENCIES:{Colors.END}
  {Colors.YELLOW}pip install -r requirements.txt{Colors.END}

{Colors.BOLD}LEGAL NOTICE:{Colors.END}
  {Colors.RED}This tool is for authorized security research and ethical use only.
  Misuse may violate privacy laws. Use responsibly.{Colors.END}

{Colors.CYAN}╔═══════════════════════════════════════════════════════════════╗
║  Author: Enhanced by Community | Version: 3.0                 ║
║  GitHub: github.com/Roti18/XTrace | License: MIT                       ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
"""
    print(help_text)

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
