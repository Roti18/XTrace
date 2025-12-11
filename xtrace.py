#!/usr/bin/env python3
import argparse
import sys
from datetime import datetime

from modules.colors import Colors
from modules.username import check_username
from modules.email import check_email
from modules.domain import check_domain
from modules.phone import check_phone
from modules.ip import check_ip
from modules.photo import check_photo
from osint_tool import XTraceOSINT, PILLOW_AVAILABLE, DNS_AVAILABLE, BS4_AVAILABLE

def main():
    """Main function"""
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
  {Colors.GREEN}-u, --username <username>{Colors.END}    Search username across 100+ platforms
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
  • Username search across 100+ social media & platforms
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
