import re
import hashlib
import socket
from datetime import datetime
from .utils import save_results, generate_report
from .colors import Colors

try:
    import dns.resolver
    DNS_AVAILABLE = True
except ImportError:
    DNS_AVAILABLE = False

def check_email(email, session_id):
    """Enhanced email OSINT dengan validasi lengkap"""
    print(f"\n{Colors.BOLD}[*] Analyzing email: {Colors.CYAN}{email}{Colors.END}")
    
    if not re.match(r'^[\w.-]+@[\w.-]+\.\w+$', email):
        print(f"{Colors.RED}[!] Invalid email format{Colors.END}")
        return None
    
    username, domain = email.split('@')
    
    print(f"\n{Colors.GREEN}[+] Username: {username}{Colors.END}")
    print(f"{Colors.GREEN}[+] Domain: {domain}{Colors.END}")
    
    results = {
        'target': email,
        'email': email,
        'username': username,
        'domain': domain,
        'validation': {},
        'hashes': {},
        'provider': {},
        'breach_check': [],
        'social_media': []
    }
    
    print(f"\n{Colors.BOLD}[*] Generating Hashes...{Colors.END}")
    email_lower = email.lower().strip()
    results['hashes'] = {
        'md5': hashlib.md5(email_lower.encode()).hexdigest(),
        'sha1': hashlib.sha1(email_lower.encode()).hexdigest(),
        'sha256': hashlib.sha256(email_lower.encode()).hexdigest()
    }
    
    print(f"  {Colors.CYAN}MD5:    {results['hashes']['md5']}{Colors.END}")
    print(f"  {Colors.CYAN}SHA1:   {results['hashes']['sha1']}{Colors.END}")
    print(f"  {Colors.CYAN}SHA256: {results['hashes']['sha256'][:50]}...{Colors.END}")
    
    print(f"\n{Colors.BOLD}[*] Provider Detection...{Colors.END}")
    providers = {
        'gmail.com': {'name': 'Google Gmail', 'type': 'Free', 'country': 'USA'},
        'yahoo.com': {'name': 'Yahoo Mail', 'type': 'Free', 'country': 'USA'},
        'outlook.com': {'name': 'Microsoft Outlook', 'type': 'Free', 'country': 'USA'},
        'hotmail.com': {'name': 'Microsoft Hotmail', 'type': 'Free', 'country': 'USA'},
        'protonmail.com': {'name': 'ProtonMail', 'type': 'Encrypted', 'country': 'Switzerland'},
        'proton.me': {'name': 'Proton Mail', 'type': 'Encrypted', 'country': 'Switzerland'},
        'icloud.com': {'name': 'Apple iCloud', 'type': 'Free', 'country': 'USA'},
        'aol.com': {'name': 'AOL Mail', 'type': 'Free', 'country': 'USA'},
        'mail.ru': {'name': 'Mail.ru', 'type': 'Free', 'country': 'Russia'},
        'yandex.com': {'name': 'Yandex Mail', 'type': 'Free', 'country': 'Russia'},
    }
    
    if domain in providers:
        results['provider'] = providers[domain]
        print(f"  {Colors.GREEN}[+] Provider: {results['provider']['name']}{Colors.END}")
        print(f"  {Colors.GREEN}[+] Type: {results['provider']['type']}{Colors.END}")
        print(f"  {Colors.GREEN}[+] Country: {results['provider']['country']}{Colors.END}")
    else:
        results['provider'] = {'name': 'Custom/Corporate Domain', 'type': 'Custom'}
        print(f"  {Colors.YELLOW}[+] Provider: Custom/Corporate Domain{Colors.END}")
    
    print(f"\n{Colors.BOLD}[*] Domain Validation...{Colors.END}")
    try:
        ip = socket.gethostbyname(domain)
        results['validation']['domain_ip'] = ip
        results['validation']['domain_valid'] = True
        print(f"  {Colors.GREEN}[✓] Domain resolves to: {ip}{Colors.END}")
        
        if DNS_AVAILABLE:
            try:
                mx_records = dns.resolver.resolve(domain, 'MX')
                results['validation']['mx_records'] = []
                print(f"  {Colors.GREEN}[✓] MX Records found:{Colors.END}")
                for mx in mx_records:
                    mx_str = str(mx).split()
                    results['validation']['mx_records'].append(mx_str)
                    print(f"      Priority {mx_str[0]}: {mx_str[1]}")
            except:
                print(f"  {Colors.YELLOW}[!] No MX records found{Colors.END}")
        else:
            print(f"  {Colors.YELLOW}[!] dnspython not installed, skipping MX record check.{Colors.END}")

    except:
        results['validation']['domain_valid'] = False
        print(f"  {Colors.RED}[×] Domain cannot be resolved{Colors.END}")
    
    print(f"\n{Colors.BOLD}[*] Data Breach Check Resources:{Colors.END}")
    breach_sites = [
        {'name': 'Have I Been Pwned', 'url': f"https://haveibeenpwned.com/account/{email}"},
        {'name': 'DeHashed', 'url': f"https://dehashed.com/search?query={email}"},
        {'name': 'LeakCheck', 'url': "https://leakcheck.io/"},
        {'name': 'IntelX', 'url': f"https://intelx.io/?s={email}"},
        {'name': 'Hunter.io', 'url': f"https://hunter.io/verify/{email}"}
    ]
    
    results['breach_check'] = breach_sites
    for site in breach_sites:
        print(f"  {Colors.CYAN}→ {site['name']}: {site['url']}{Colors.END}")
    
    print(f"\n{Colors.BOLD}[*] Social Media & Web Presence:{Colors.END}")
    social_checks = [
        {'name': 'Gravatar', 'url': f"https://gravatar.com/{results['hashes']['md5']}"},
        {'name': 'Google Search', 'url': f"https://www.google.com/search?q=\"{email}\""},
        {'name': 'GitHub', 'url': f"https://github.com/search?q={email}&type=users"},
        {'name': 'Twitter', 'url': f"https://twitter.com/search?q={email}"},
    ]
    
    results['social_media'] = social_checks
    for check in social_checks:
        print(f"  {Colors.CYAN}→ {check['name']}: {check['url']}{Colors.END}")
    
    print(f"\n{Colors.BOLD}[*] Possible Username Variations:{Colors.END}")
    variations = [
        username,
        username.replace('.', ''),
        username.replace('_', ''),
        username.split('.')[0] if '.' in username else username,
    ]
    
    for var in set(variations):
        print(f"  {Colors.YELLOW}• {var}{Colors.END}")
    
    results['username_variations'] = list(set(variations))
    
    save_results('email', results, session_id)
    generate_report('email', results, session_id)
    
    return results
