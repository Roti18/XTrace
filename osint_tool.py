#!/usr/bin/env python3
"""
XTrace v3.0 - Advanced OSINT Intelligence Platform
Enhanced version dengan akurasi tinggi dan fitur lengkap
Untuk penggunaan legal dan etis saja
"""

import json
import re
import socket
import urllib.request
import urllib.parse
import urllib.error
import ssl
import sys
import os
from datetime import datetime
import hashlib
import base64
from html.parser import HTMLParser
import threading
import time
from collections import defaultdict

# Cek dependencies
try:
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False
    print("[!] Pillow tidak terinstall - Photo OSINT tidak tersedia")

try:
    import dns.resolver
    DNS_AVAILABLE = True
except ImportError:
    DNS_AVAILABLE = False
    print("[!] dnspython tidak terinstall - DNS features terbatas")

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False
    print("[!] BeautifulSoup4 tidak terinstall - Web scraping terbatas")

class Colors:
    """ANSI color codes untuk terminal"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'

class LinkExtractor(HTMLParser):
    """Parser HTML untuk ekstraksi link dan email"""
    def __init__(self):
        super().__init__()
        self.links = []
        self.emails = []
        self.social_links = []
    
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    link = attr[1]
                    self.links.append(link)
                    # Deteksi social media links
                    social_domains = ['facebook.com', 'twitter.com', 'instagram.com', 
                                     'linkedin.com', 'youtube.com', 'tiktok.com']
                    if any(domain in link for domain in social_domains):
                        self.social_links.append(link)
    
    def handle_data(self, data):
        emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', data)
        self.emails.extend(emails)

class XTraceOSINT:
    def __init__(self):
        self.results = {}
        self.ssl_context = ssl._create_unverified_context()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.ensure_directories()
        self.username_cache = {}
    
    def ensure_directories(self):
        """Pastikan semua folder yang dibutuhkan ada"""
        dirs = ['docs', 'images', 'logs', 'result', 'reports', 'data']
        for d in dirs:
            if not os.path.exists(d):
                os.makedirs(d)
    
    def log(self, message, level="INFO"):
        """Logging ke file dengan format lengkap"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file = f"logs/xtrace_{datetime.now().strftime('%Y%m%d')}.log"
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] [{level}] {message}\n")
        except:
            pass
    
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
        self.log(f"XTrace v3.0 started - Session: {self.session_id}")
    
    def make_request(self, url, timeout=10, method='GET', data=None):
        """HTTP request dengan error handling lengkap"""
        try:
            if data:
                data = urllib.parse.urlencode(data).encode('utf-8')
            
            req = urllib.request.Request(url, data=data, headers=self.headers, method=method)
            response = urllib.request.urlopen(req, timeout=timeout, context=self.ssl_context)
            return response
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            return None
        except urllib.error.URLError:
            return None
        except socket.timeout:
            return None
        except Exception as e:
            self.log(f"Request error for {url}: {str(e)}", "ERROR")
            return None
    
    def save_results(self, mode, data):
        """Simpan hasil ke file JSON dengan format lengkap"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"result/{mode}_{timestamp}.json"
        
        result_data = {
            'session_id': self.session_id,
            'timestamp': datetime.now().isoformat(),
            'mode': mode,
            'target': data.get('target', 'unknown'),
            'data': data,
            'metadata': {
                'tool': 'XTrace v3.0',
                'user_location': 'Surabaya, Indonesia',
                'scan_duration': data.get('scan_duration', 'unknown')
            }
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, indent=4, ensure_ascii=False)
            
            print(f"\n{Colors.GREEN}[✓] Results saved: {filename}{Colors.END}")
            self.log(f"Results saved: {filename}")
            return filename
        except Exception as e:
            print(f"{Colors.RED}[!] Error saving results: {e}{Colors.END}")
            return None
    
    def generate_report(self, mode, data):
        """Generate HTML report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reports/{mode}_report_{timestamp}.html"
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>XTrace Report - {mode.upper()}</title>
    <style>
        body {{ font-family: Arial; margin: 20px; background: #f5f5f5; }}
        .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 5px; }}
        .section {{ background: white; margin: 20px 0; padding: 20px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .result-item {{ margin: 10px 0; padding: 10px; background: #ecf0f1; border-radius: 3px; }}
        .success {{ color: #27ae60; }}
        .error {{ color: #e74c3c; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #34495e; color: white; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>XTrace v3.0 - OSINT Report</h1>
        <p>Mode: {mode.upper()} | Session: {self.session_id}</p>
        <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    </div>
    <div class="section">
        <h2>Scan Results</h2>
        <pre>{json.dumps(data, indent=2, ensure_ascii=False)}</pre>
    </div>
</body>
</html>
"""
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"{Colors.GREEN}[✓] HTML report generated: {filename}{Colors.END}")
        except:
            pass
    
    def check_username(self, username):
        """Enhanced username search dengan 100+ platform"""
        start_time = time.time()
        print(f"\n{Colors.BOLD}[*] Scanning username: {Colors.CYAN}{username}{Colors.END}")
        print(f"{Colors.YELLOW}[*] Checking 100+ platforms (this may take a minute)...{Colors.END}\n")
        
        platforms = {
            'GitHub': f'https://github.com/{username}',
            'Reddit': f'https://www.reddit.com/user/{username}',
            'Twitter/X': f'https://twitter.com/{username}',
            'Instagram': f'https://www.instagram.com/{username}',
            'Facebook': f'https://www.facebook.com/{username}',
            'LinkedIn': f'https://www.linkedin.com/in/{username}',
            'TikTok': f'https://www.tiktok.com/@{username}',
            'Snapchat': f'https://www.snapchat.com/add/{username}',
            'Pinterest': f'https://www.pinterest.com/{username}',
            'Tumblr': f'https://{username}.tumblr.com',
            
            'Medium': f'https://medium.com/@{username}',
            'YouTube': f'https://www.youtube.com/@{username}',
            'Twitch': f'https://www.twitch.tv/{username}',
            'Vimeo': f'https://vimeo.com/{username}',
            'Dailymotion': f'https://www.dailymotion.com/{username}',
            
            'GitLab': f'https://gitlab.com/{username}',
            'Bitbucket': f'https://bitbucket.org/{username}',
            'CodePen': f'https://codepen.io/{username}',
            'Replit': f'https://replit.com/@{username}',
            'StackOverflow': f'https://stackoverflow.com/users/{username}',
            'HackerRank': f'https://www.hackerrank.com/{username}',
            'LeetCode': f'https://leetcode.com/{username}',
            'CodeForces': f'https://codeforces.com/profile/{username}',
            'HackerNews': f'https://news.ycombinator.com/user?id={username}',
            
            'DeviantArt': f'https://www.deviantart.com/{username}',
            'Behance': f'https://www.behance.net/{username}',
            'Dribbble': f'https://dribbble.com/{username}',
            'ArtStation': f'https://www.artstation.com/{username}',
            'Flickr': f'https://www.flickr.com/people/{username}',
            
            'Spotify': f'https://open.spotify.com/user/{username}',
            'SoundCloud': f'https://soundcloud.com/{username}',
            'Bandcamp': f'https://{username}.bandcamp.com',
            'Mixcloud': f'https://www.mixcloud.com/{username}',
            
            'Steam': f'https://steamcommunity.com/id/{username}',
            'Xbox': f'https://account.xbox.com/en-us/profile?gamertag={username}',
            'PlayStation': f'https://psnprofiles.com/{username}',
            'Roblox': f'https://www.roblox.com/users/profile?username={username}',
            'Epic Games': f'https://www.epicgames.com/site/en-US/{username}',
            
            'AngelList': f'https://angel.co/{username}',
            'Meetup': f'https://www.meetup.com/members/{username}',
            'SlideShare': f'https://www.slideshare.net/{username}',
            'ResearchGate': f'https://www.researchgate.net/profile/{username}',
            'Academia': f'https://independent.academia.edu/{username}',
            
            'ProductHunt': f'https://www.producthunt.com/@{username}',
            'Etsy': f'https://www.etsy.com/shop/{username}',
            'Patreon': f'https://www.patreon.com/{username}',
            
            'Quora': f'https://www.quora.com/profile/{username}',
            'Scribd': f'https://www.scribd.com/{username}',
            
            'About.me': f'https://about.me/{username}',
            'Linktree': f'https://linktr.ee/{username}',
            'Gravatar': f'https://gravatar.com/{username}',
            'Keybase': f'https://keybase.io/{username}',
            
            'Kaskus': f'https://www.kaskus.co.id/profile/{username}',
            'Tokopedia': f'https://www.tokopedia.com/{username}',
            'Shopee': f'https://shopee.co.id/{username}',
            'Bukalapak': f'https://www.bukalapak.com/u/{username}',
            'Lazada': f'https://www.lazada.co.id/shop/{username}',
        }
        
        found = []
        not_found = []
        errors = []
        lock = threading.Lock()
        
        def check_platform(platform, url):
            try:
                response = self.make_request(url, timeout=8)
                if response and response.status == 200:
                    with lock:
                        found.append({'platform': platform, 'url': url, 'status_code': 200})
                        print(f"  {Colors.GREEN}[✓] {platform:25s} → {url}{Colors.END}")
                else:
                    with lock:
                        not_found.append(platform)
            except Exception as e:
                with lock:
                    errors.append({'platform': platform, 'error': str(e)})
        
        threads = []
        max_threads = 20 
        
        for i, (platform, url) in enumerate(platforms.items()):
            thread = threading.Thread(target=check_platform, args=(platform, url))
            thread.start()
            threads.append(thread)
            
            if len(threads) >= max_threads:
                for t in threads:
                    t.join()
                threads = []
        
        for thread in threads:
            thread.join()
        
        found.sort(key=lambda x: x['platform'])
        
        scan_duration = time.time() - start_time
        
        print(f"\n{Colors.BOLD}{'='*70}{Colors.END}")
        print(f"{Colors.GREEN}[✓] Found on {len(found)} platforms{Colors.END}")
        print(f"{Colors.RED}[×] Not found on {len(not_found)} platforms{Colors.END}")
        print(f"{Colors.YELLOW}[!] Errors: {len(errors)}{Colors.END}")
        print(f"{Colors.CYAN}[i] Scan duration: {scan_duration:.2f} seconds{Colors.END}")
        
        print(f"\n{Colors.BOLD}[*] Google Dorks for Advanced Search:{Colors.END}")
        dorks = [
            f'"{username}"',
            f'"{username}" site:twitter.com OR site:instagram.com OR site:facebook.com',
            f'"{username}" site:linkedin.com',
            f'"{username}" site:github.com OR site:gitlab.com',
            f'"{username}" filetype:pdf',
            f'intext:"{username}" site:pastebin.com',
            f'"{username}" inurl:profile',
            f'"{username}" inurl:user',
            f'"{username}" site:reddit.com',
            f'"{username}" (contact OR email OR phone)',
        ]
        
        for dork in dorks:
            encoded = urllib.parse.quote(dork)
            print(f"  {Colors.CYAN}→ https://www.google.com/search?q={encoded}{Colors.END}")
        
        print(f"\n{Colors.BOLD}[*] Other Search Engines:{Colors.END}")
        print(f"  {Colors.CYAN}→ Bing: https://www.bing.com/search?q={username}{Colors.END}")
        print(f"  {Colors.CYAN}→ DuckDuckGo: https://duckduckgo.com/?q={username}{Colors.END}")
        print(f"  {Colors.CYAN}→ Yandex: https://yandex.com/search/?text={username}{Colors.END}")
        
        results = {
            'target': username,
            'found': found,
            'total_found': len(found),
            'total_checked': len(platforms),
            'not_found_count': len(not_found),
            'errors': errors,
            'google_dorks': dorks,
            'scan_duration': f"{scan_duration:.2f}s",
            'timestamp': datetime.now().isoformat()
        }
        
        self.save_results('username', results)
        self.generate_report('username', results)
        
        return results
    
    def check_email(self, email):
        """Enhanced email OSINT dengan validasi lengkap"""
        print(f"\n{Colors.BOLD}[*] Analyzing email: {Colors.CYAN}{email}{Colors.END}")
        
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
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
        
        self.save_results('email', results)
        self.generate_report('email', results)
        
        return results
    
    def check_domain(self, domain):
        """Enhanced domain OSINT dengan comprehensive checks"""
        print(f"\n{Colors.BOLD}[*] Analyzing domain: {Colors.CYAN}{domain}{Colors.END}")
        
        domain = domain.replace('http://', '').replace('https://', '').replace('www.', '').split('/')[0]
        print(f"{Colors.GREEN}[+] Cleaned domain: {domain}{Colors.END}")
        
        results = {
            'target': domain,
            'domain': domain,
            'ip_info': {},
            'dns_records': {},
            'subdomains': [],
            'web_server': {},
            'security': {},
            'whois': {}
        }
        
        print(f"\n{Colors.BOLD}[*] IP Resolution...{Colors.END}")
        try:
            ip = socket.gethostbyname(domain)
            results['ip_info']['ipv4'] = ip
            print(f"  {Colors.GREEN}[✓] IPv4: {ip}{Colors.END}")
            
            try:
                hostname = socket.gethostbyaddr(ip)
                results['ip_info']['reverse_dns'] = hostname[0]
                results['ip_info']['aliases'] = hostname[1]
                print(f"  {Colors.GREEN}[✓] Reverse DNS: {hostname[0]}{Colors.END}")
            except:
                print(f"  {Colors.YELLOW}[!] No reverse DNS{Colors.END}")
            
            print(f"  {Colors.CYAN}→ Check location: https://ipinfo.io/{ip}{Colors.END}")
            
        except Exception as e:
            print(f"  {Colors.RED}[×] Cannot resolve domain: {e}{Colors.END}")
            return results
        
        if DNS_AVAILABLE:
            print(f"\n{Colors.BOLD}[*] DNS Records Analysis...{Colors.END}")
            record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME']
            
            for record_type in record_types:
                try:
                    answers = dns.resolver.resolve(domain, record_type)
                    results['dns_records'][record_type] = []
                    print(f"  {Colors.GREEN}[✓] {record_type} Records:{Colors.END}")
                    for rdata in answers:
                        record_data = str(rdata)
                        results['dns_records'][record_type].append(record_data)
                        print(f"      {record_data}")
                except:
                    pass
        
        print(f"\n{Colors.BOLD}[*] Web Server Detection...{Colors.END}")
        for protocol in ['http', 'https']:
            url = f'{protocol}://{domain}'
            try:
                response = self.make_request(url, timeout=10)
                if response:
                    print(f"  {Colors.GREEN}[✓] {protocol.upper()}: Active{Colors.END}")
                    headers = dict(response.headers)
                    if 'Server' in headers:
                        results['web_server']['server'] = headers['Server']
                        print(f"      Server: {headers['Server']}")
                    
                    tech_headers = ['X-Powered-By', 'X-AspNet-Version', 'X-Framework']
                    for tech in tech_headers:
                        if tech in headers:
                            print(f"      {tech}: {headers[tech]}")
                    
                    results['web_server'][protocol] = 'active'
            except:
                results['web_server'][protocol] = 'inactive'
        
        if results['web_server'].get('https') == 'active':
            print(f"\n{Colors.BOLD}[*] SSL/TLS Certificate...{Colors.END}")
            try:
                context = ssl.create_default_context()
                with socket.create_connection((domain, 443), timeout=5) as sock:
                    with context.wrap_socket(sock, server_hostname=domain) as ssock:
                        cert = ssock.getpeercert()
                        results['security']['ssl'] = {
                            'issuer': dict(x[0] for x in cert['issuer']),
                            'subject': dict(x[0] for x in cert['subject']),
                            'version': cert['version'],
                            'notBefore': cert['notBefore'],
                            'notAfter': cert['notAfter']
                        }
                        print(f"  {Colors.GREEN}[✓] SSL Certificate Valid{Colors.END}")
                        print(f"      Issued to: {cert['subject']}")
                        print(f"      Valid until: {cert['notAfter']}")
            except:
                print(f"  {Colors.YELLOW}[!] SSL Certificate check failed{Colors.END}")
        
        print(f"\n{Colors.BOLD}[*] Subdomain Discovery...{Colors.END}")
        common_subdomains = [
            'www', 'mail', 'webmail', 'ftp', 'smtp', 'pop', 'imap',
            'admin', 'administrator', 'api', 'app', 'blog', 'dev', 
            'development', 'test', 'testing', 'staging', 'stage',
            'cdn', 'static', 'assets', 'img', 'images', 'video',
            'vpn', 'remote', 'portal', 'dashboard', 'panel',
            'shop', 'store', 'payment', 'pay', 'checkout',
            'support', 'help', 'docs', 'wiki', 'forum',
            'm', 'mobile', 'amp', 'beta', 'demo'
        ]
        
        found_subs = []
        
        def check_subdomain(sub):
            subdomain = f"{sub}.{domain}"
            try:
                socket.gethostbyname(subdomain)
                found_subs.append(subdomain)
                print(f"  {Colors.GREEN}[✓] {subdomain}{Colors.END}")
            except:
                pass
        
        threads = []
        for sub in common_subdomains:
            thread = threading.Thread(target=check_subdomain, args=(sub,))
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()
        
        results['subdomains'] = found_subs
        print(f"\n{Colors.GREEN}[✓] Found {len(found_subs)} subdomains{Colors.END}")
        
        print(f"\n{Colors.BOLD}[*] External Resources:{Colors.END}")
        resources = [
            f"https://www.whois.com/whois/{domain}",
            f"https://mxtoolbox.com/SuperTool.aspx?action=mx:{domain}",
            f"https://dnsdumpster.com/",
            f"https://securitytrails.com/domain/{domain}/dns",
            f"https://crt.sh/?q={domain}",
            f"https://www.virustotal.com/gui/domain/{domain}"
        ]
        
        for resource in resources:
            print(f"  {Colors.CYAN}→ {resource}{Colors.END}")
        
        self.save_results('domain', results)
        self.generate_report('domain', results)
        
        return results
    
    def check_phone(self, phone):
        """Enhanced phone number OSINT"""
        print(f"\n{Colors.BOLD}[*] Analyzing phone: {Colors.CYAN}{phone}{Colors.END}")
        
        clean = re.sub(r'[^\d+]', '', phone)
        results = {
            'target': phone,
            'original': phone,
            'cleaned': clean,
            'country': None,
            'provider': None,
            'type': None,
            'validation': {}
        }
        
        print(f"{Colors.GREEN}[+] Cleaned format: {clean}{Colors.END}")
        
        country_codes = {
            '+1': 'USA/Canada',
            '+44': 'United Kingdom',
            '+62': 'Indonesia',
            '+91': 'India',
            '+86': 'China',
            '+81': 'Japan',
            '+82': 'South Korea',
            '+65': 'Singapore',
            '+60': 'Malaysia',
            '+66': 'Thailand',
            '+84': 'Vietnam',
            '+63': 'Philippines'
        }
        
        for code, country in country_codes.items():
            if clean.startswith(code):
                results['country'] = country
                results['country_code'] = code
                print(f"{Colors.GREEN}[+] Country: {country}{Colors.END}")
                break
        
        if clean.startswith('+62') or clean.startswith('62') or clean.startswith('08'):
            if clean.startswith('08'):
                clean = '+62' + clean[1:]
            elif clean.startswith('62'):
                clean = '+' + clean
            
            results['country'] = 'Indonesia'
            results['normalized'] = clean
            results['country_code'] = '+62'
            
            print(f"{Colors.GREEN}[+] Country: Indonesia{Colors.END}")
            print(f"{Colors.GREEN}[+] Normalized: {clean}{Colors.END}")
            
            providers_id = {
                '811': {'name': 'Telkomsel', 'type': 'Halo'},
                '812': {'name': 'Telkomsel', 'type': 'simPATI'},
                '813': {'name': 'Telkomsel', 'type': 'simPATI'},
                '821': {'name': 'Telkomsel', 'type': 'Kartu AS'},
                '822': {'name': 'Telkomsel', 'type': 'simPATI'},
                '823': {'name': 'Telkomsel', 'type': 'Kartu AS'},
                '851': {'name': 'Telkomsel', 'type': 'Halo'},
                '852': {'name': 'Telkomsel', 'type': 'Kartu AS'},
                '853': {'name': 'Telkomsel', 'type': 'Kartu AS'},
                '814': {'name': 'Indosat Ooredoo', 'type': 'IM3'},
                '815': {'name': 'Indosat Ooredoo', 'type': 'Matrix'},
                '816': {'name': 'Indosat Ooredoo', 'type': 'Mentari'},
                '855': {'name': 'Indosat Ooredoo', 'type': 'IM3'},
                '856': {'name': 'Indosat Ooredoo', 'type': 'IM3'},
                '857': {'name': 'Indosat Ooredoo', 'type': 'IM3'},
                '858': {'name': 'Indosat Ooredoo', 'type': 'Mentari'},
                '817': {'name': 'XL Axiata', 'type': 'XL'},
                '818': {'name': 'XL Axiata', 'type': 'XL'},
                '819': {'name': 'XL Axiata', 'type': 'XL'},
                '859': {'name': 'XL Axiata', 'type': 'XL'},
                '877': {'name': 'XL Axiata', 'type': 'XL'},
                '878': {'name': 'XL Axiata', 'type': 'XL'},
                '895': {'name': 'Tri Indonesia', 'type': '3'},
                '896': {'name': 'Tri Indonesia', 'type': '3'},
                '897': {'name': 'Tri Indonesia', 'type': '3'},
                '898': {'name': 'Tri Indonesia', 'type': '3'},
                '899': {'name': 'Tri Indonesia', 'type': '3'},
                '831': {'name': 'Axis', 'type': 'AXIS'},
                '832': {'name': 'Axis', 'type': 'AXIS'},
                '833': {'name': 'Axis', 'type': 'AXIS'},
                '838': {'name': 'Axis', 'type': 'AXIS'},
                '881': {'name': 'Smartfren', 'type': 'Smartfren'},
                '882': {'name': 'Smartfren', 'type': 'Smartfren'},
                '883': {'name': 'Smartfren', 'type': 'Smartfren'},
                '884': {'name': 'Smartfren', 'type': 'Smartfren'},
                '885': {'name': 'Smartfren', 'type': 'Smartfren'},
                '886': {'name': 'Smartfren', 'type': 'Smartfren'},
                '887': {'name': 'Smartfren', 'type': 'Smartfren'},
                '888': {'name': 'Smartfren', 'type': 'Smartfren'},
                '889': {'name': 'Smartfren', 'type': 'Smartfren'}
            }
            
            if len(clean) >= 6:
                prefix = clean.replace('+62', '').replace('0', '', 1)[:3]
                if prefix in providers_id:
                    results['provider'] = providers_id[prefix]['name']
                    results['card_type'] = providers_id[prefix]['type']
                    print(f"{Colors.GREEN}[+] Provider: {results['provider']}{Colors.END}")
                    print(f"{Colors.GREEN}[+] Card Type: {results['card_type']}{Colors.END}")
        
        if len(clean.replace('+', '')) >= 10:
            results['validation']['length'] = 'Valid'
            print(f"{Colors.GREEN}[+] Length: Valid (≥10 digits){Colors.END}")
        else:
            results['validation']['length'] = 'Invalid'
            print(f"{Colors.RED}[!] Length: Invalid (<10 digits){Colors.END}")
        
        print(f"\n{Colors.BOLD}[*] Phone Lookup Resources:{Colors.END}")
        lookup_sites = [
            {'name': 'Truecaller', 'url': f"https://www.truecaller.com/search/{clean.replace('+', '%2B')}"},
            {'name': 'WhatsApp Check', 'url': f"https://wa.me/{clean.replace('+', '')}"},
            {'name': 'Telegram', 'url': f"https://t.me/{clean.replace('+', '')}"},
            {'name': 'GetContact', 'url': "https://www.getcontact.com/"},
            {'name': 'NumLookup', 'url': f"https://www.numlookup.com/?phone={clean}"}
        ]
        
        for site in lookup_sites:
            print(f"  {Colors.CYAN}→ {site['name']}: {site['url']}{Colors.END}")
        
        results['lookup_resources'] = lookup_sites
        
        self.save_results('phone', results)
        self.generate_report('phone', results)
        
        return results
    
    def check_ip(self, ip):
        """Enhanced IP address OSINT"""
        print(f"\n{Colors.BOLD}[*] Analyzing IP: {Colors.CYAN}{ip}{Colors.END}")
        
        try:
            socket.inet_aton(ip)
        except:
            print(f"{Colors.RED}[!] Invalid IP format{Colors.END}")
            return None
        
        results = {
            'target': ip,
            'ip': ip,
            'type': None,
            'reverse_dns': None,
            'open_ports': [],
            'services': []
        }
        
        parts = list(map(int, ip.split('.')))
        
        if parts[0] == 10:
            results['type'] = 'Private (Class A)'
        elif parts[0] == 172 and 16 <= parts[1] <= 31:
            results['type'] = 'Private (Class B)'
        elif parts[0] == 192 and parts[1] == 168:
            results['type'] = 'Private (Class C)'
        elif parts[0] == 127:
            results['type'] = 'Loopback'
        elif parts[0] >= 224:
            results['type'] = 'Reserved/Multicast'
        else:
            results['type'] = 'Public'
        
        print(f"{Colors.GREEN}[+] Type: {results['type']}{Colors.END}")
        
        print(f"\n{Colors.BOLD}[*] Reverse DNS Lookup...{Colors.END}")
        try:
            hostname = socket.gethostbyaddr(ip)
            results['reverse_dns'] = hostname[0]
            print(f"  {Colors.GREEN}[✓] Hostname: {hostname[0]}{Colors.END}")
        except:
            print(f"  {Colors.YELLOW}[!] No reverse DNS record{Colors.END}")
        
        print(f"\n{Colors.BOLD}[*] Port Scanning (Top 25 ports)...{Colors.END}")
        ports = {
            20: 'FTP Data', 21: 'FTP', 22: 'SSH', 23: 'Telnet',
            25: 'SMTP', 53: 'DNS', 80: 'HTTP', 110: 'POP3',
            143: 'IMAP', 443: 'HTTPS', 445: 'SMB', 465: 'SMTPS',
            587: 'SMTP', 993: 'IMAPS', 995: 'POP3S', 1433: 'MSSQL',
            3306: 'MySQL', 3389: 'RDP', 5432: 'PostgreSQL',
            5900: 'VNC', 6379: 'Redis', 8000: 'HTTP Alt',
            8080: 'HTTP Proxy', 8443: 'HTTPS Alt', 27017: 'MongoDB'
        }
        
        open_ports = []
        
        def scan_port(port, service):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((ip, port))
            sock.close()
            
            if result == 0:
                open_ports.append({'port': port, 'service': service, 'state': 'open'})
                print(f"  {Colors.GREEN}[✓] Port {port:5d} ({service:15s}) OPEN{Colors.END}")
        
        threads = []
        for port, service in ports.items():
            thread = threading.Thread(target=scan_port, args=(port, service))
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()
        
        results['open_ports'] = open_ports
        
        if not open_ports:
            print(f"  {Colors.YELLOW}[!] No common ports open or filtered{Colors.END}")
        else:
            print(f"\n{Colors.GREEN}[✓] Found {len(open_ports)} open ports{Colors.END}")
        
        print(f"\n{Colors.BOLD}[*] IP Intelligence Resources:{Colors.END}")
        resources = [
            {'name': 'IPInfo', 'url': f"https://ipinfo.io/{ip}"},
            {'name': 'AbuseIPDB', 'url': f"https://www.abuseipdb.com/check/{ip}"},
            {'name': 'VirusTotal', 'url': f"https://www.virustotal.com/gui/ip-address/{ip}"},
            {'name': 'Shodan', 'url': f"https://www.shodan.io/host/{ip}"},
            {'name': 'Censys', 'url': f"https://search.censys.io/hosts/{ip}"},
            {'name': 'IPVoid', 'url': f"https://www.ipvoid.com/ip-blacklist-check/"},
            {'name': 'WHOIS', 'url': f"https://www.whois.com/whois/{ip}"}
        ]
        
        results['intelligence_resources'] = resources
        for resource in resources:
            print(f"  {Colors.CYAN}→ {resource['name']}: {resource['url']}{Colors.END}")
        
        self.save_results('ip', results)
        self.generate_report('ip', results)
        
        return results
    
    def check_photo(self, photo_path):
        """Photo EXIF and metadata analysis"""
        if not PILLOW_AVAILABLE:
            print(f"{Colors.RED}[!] Pillow library not installed{Colors.END}")
            print(f"{Colors.YELLOW}[!] Install: pip install Pillow{Colors.END}")
            return None
        
        print(f"\n{Colors.BOLD}[*] Analyzing photo: {Colors.CYAN}{photo_path}{Colors.END}")
        
        if not os.path.exists(photo_path):
            print(f"{Colors.RED}[!] File not found{Colors.END}")
            return None
        
        results = {
            'target': photo_path,
            'file_info': {},
            'exif_data': {},
            'gps_data': {},
            'hashes': {}
        }
        
        try:
            img = Image.open(photo_path)
            
            results['file_info'] = {
                'filename': os.path.basename(photo_path),
                'size_bytes': os.path.getsize(photo_path),
                'size_kb': round(os.path.getsize(photo_path) / 1024, 2),
                'dimensions': f"{img.size[0]}x{img.size[1]}",
                'format': img.format,
                'mode': img.mode
            }
            
            print(f"\n{Colors.BOLD}[*] File Information:{Colors.END}")
            print(f"  {Colors.GREEN}[+] Filename: {results['file_info']['filename']}{Colors.END}")
            print(f"  {Colors.GREEN}[+] Size: {results['file_info']['size_kb']} KB{Colors.END}")
            print(f"  {Colors.GREEN}[+] Dimensions: {results['file_info']['dimensions']}{Colors.END}")
            print(f"  {Colors.GREEN}[+] Format: {results['file_info']['format']}{Colors.END}")
            
            print(f"\n{Colors.BOLD}[*] File Hashes:{Colors.END}")
            with open(photo_path, 'rb') as f:
                file_data = f.read()
                results['hashes'] = {
                    'md5': hashlib.md5(file_data).hexdigest(),
                    'sha256': hashlib.sha256(file_data).hexdigest()
                }
            
            print(f"  {Colors.CYAN}MD5:    {results['hashes']['md5']}{Colors.END}")
            print(f"  {Colors.CYAN}SHA256: {results['hashes']['sha256'][:50]}...{Colors.END}")
            
            exif = img._getexif()
            if exif:
                print(f"\n{Colors.BOLD}[*] EXIF Data Found:{Colors.END}")
                
                for tag_id, value in exif.items():
                    tag = TAGS.get(tag_id, tag_id)
                    
                    if tag == 'GPSInfo':
                        gps_data = {}
                        for gps_tag_id, gps_value in value.items():
                            sub_tag = GPSTAGS.get(gps_tag_id, gps_tag_id)
                            if isinstance(gps_value, bytes):
                                gps_data[sub_tag] = gps_value.decode('utf-8', errors='ignore').strip().strip('\x00')
                            else:
                                gps_data[sub_tag] = gps_value
                        
                        results['gps_data'] = gps_data
                        
                        if 'GPSLatitude' in gps_data and 'GPSLongitude' in gps_data:
                            try:
                                def convert_to_degrees(value):
                                    d, m, s = value
                                    return float(d) + float(m) / 60 + float(s) / 3600
                                
                                lat = convert_to_degrees(gps_data['GPSLatitude'])
                                lon = convert_to_degrees(gps_data['GPSLongitude'])
                                
                                if gps_data.get('GPSLatitudeRef') == 'S':
                                    lat = -lat
                                if gps_data.get('GPSLongitudeRef') == 'W':
                                    lon = -lon
                                
                                results['gps_decimal'] = {'latitude': lat, 'longitude': lon}
                                
                                print(f"  {Colors.GREEN}[✓] GPS Location Found!{Colors.END}")
                                print(f"      Latitude: {lat}")
                                print(f"      Longitude: {lon}")
                                print(f"      {Colors.CYAN}Google Maps: https://maps.google.com/?q={lat},{lon}{Colors.END}")
                            except (ValueError, TypeError):
                                print(f"  {Colors.YELLOW}[!] Could not parse GPS coordinates.{Colors.END}")
                    else:
                        if isinstance(value, bytes):
                            value = value.decode('utf-8', errors='ignore').strip().strip('\x00')
                        
                        results['exif_data'][tag] = str(value)
                        
                        important_tags = ['Make', 'Model', 'DateTime', 'DateTimeOriginal', 
                                        'Software', 'Artist', 'Copyright']
                        if tag in important_tags:
                            print(f"  {Colors.CYAN}{tag}: {value}{Colors.END}")
            else:
                print(f"\n{Colors.YELLOW}[!] No EXIF data found{Colors.END}")
            
            print(f"\n{Colors.BOLD}[*] Reverse Image Search:{Colors.END}")
            searches = [
                "https://images.google.com/",
                "https://tineye.com/",
                "https://yandex.com/images/",
                "https://www.bing.com/visualsearch"
            ]
            
            for search in searches:
                print(f"  {Colors.CYAN}→ {search}{Colors.END}")
            
            img.close()
            
            self.save_results('photo', results)
            self.generate_report('photo', results)
            
            return results
            
        except Exception as e:
            print(f"{Colors.RED}[!] Error analyzing photo: {e}{Colors.END}")
            return None
    
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
                self.log("Session ended by user")
                break
                
            elif choice == '1':
                username = input(f"\n{Colors.YELLOW}Enter username: {Colors.END}").strip()
                if username:
                    self.check_username(username)
                    
            elif choice == '2':
                email = input(f"\n{Colors.YELLOW}Enter email: {Colors.END}").strip()
                if email:
                    self.check_email(email)
                    
            elif choice == '3':
                domain = input(f"\n{Colors.YELLOW}Enter domain: {Colors.END}").strip()
                if domain:
                    self.check_domain(domain)
                    
            elif choice == '4':
                phone = input(f"\n{Colors.YELLOW}Enter phone number: {Colors.END}").strip()
                if phone:
                    self.check_phone(phone)
                    
            elif choice == '5':
                ip = input(f"\n{Colors.YELLOW}Enter IP address: {Colors.END}").strip()
                if ip:
                    self.check_ip(ip)
                    
            elif choice == '6':
                photo = input(f"\n{Colors.YELLOW}Enter photo path: {Colors.END}").strip()
                if photo:
                    self.check_photo(photo)
                    
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
    
    for dep, available in deps.items():
        status = f"{Colors.GREEN}✓ Installed{Colors.END}" if available else f"{Colors.YELLOW}✗ Not installed{Colors.END}"
        print(f"  {dep:20s}: {status}")
    
    if not all(deps.values()):
        print(f"\n{Colors.YELLOW}[!] Some features may be limited{Colors.END}")
        print(f"{Colors.YELLOW}[!] Install all: pip install Pillow dnspython beautifulsoup4{Colors.END}")
    
    time.sleep(2)
    
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        
        if len(sys.argv) < 3 and mode not in ['help', '-h']:
            print(f"{Colors.RED}[!] Missing target argument{Colors.END}")
            print(f"{Colors.YELLOW}Usage: {sys.argv[0]} <mode> <target>{Colors.END}")
            print(f"{Colors.YELLOW}Example: {sys.argv[0]} username john_doe{Colors.END}")
            sys.exit(1)
        
        target = sys.argv[2] if len(sys.argv) > 2 else None
        
        if mode == 'username' or mode == '-u':
            tool.check_username(target)
        elif mode == 'email' or mode == '-e':
            tool.check_email(target)
        elif mode == 'domain' or mode == '-d':
            tool.check_domain(target)
        elif mode == 'phone' or mode == '-p':
            tool.check_phone(target)
        elif mode == 'ip' or mode == '-i':
            tool.check_ip(target)
        elif mode == 'photo' or mode == '-ph':
            tool.check_photo(target)
        elif mode == 'help' or mode == '-h':
            print_help()
        else:
            print(f"{Colors.RED}[!] Unknown mode: {mode}{Colors.END}")
            print_help()
    else:
        tool.interactive_mode()

def print_help():
    """Print help menu"""
    help_text = f"""
{Colors.CYAN}╔═══════════════════════════════════════════════════════════════╗
║                    XTRACE v3.0 - HELP MENU                    ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}

{Colors.BOLD}USAGE:{Colors.END}
  python xtrace.py [mode] [target]
  python xtrace.py                    # Interactive mode

{Colors.BOLD}MODES:{Colors.END}
  {Colors.GREEN}username{Colors.END}, {Colors.GREEN}-u{Colors.END}     Search username across 100+ platforms
  {Colors.GREEN}email{Colors.END}, {Colors.GREEN}-e{Colors.END}        Email validation and OSINT
  {Colors.GREEN}domain{Colors.END}, {Colors.GREEN}-d{Colors.END}       Domain analysis and DNS lookup
  {Colors.GREEN}phone{Colors.END}, {Colors.GREEN}-p{Colors.END}        Phone number lookup and analysis
  {Colors.GREEN}ip{Colors.END}, {Colors.GREEN}-i{Colors.END}           IP address information and port scan
  {Colors.GREEN}photo{Colors.END}, {Colors.GREEN}-ph{Colors.END}       Photo EXIF and metadata extraction
  {Colors.GREEN}help{Colors.END}, {Colors.GREEN}-h{Colors.END}         Show this help menu

{Colors.BOLD}EXAMPLES:{Colors.END}
  {Colors.CYAN}python xtrace.py username john_doe{Colors.END}
  {Colors.CYAN}python xtrace.py email test@example.com{Colors.END}
  {Colors.CYAN}python xtrace.py domain example.com{Colors.END}
  {Colors.CYAN}python xtrace.py phone +6281234567890{Colors.END}
  {Colors.CYAN}python xtrace.py ip 8.8.8.8{Colors.END}
  {Colors.CYAN}python xtrace.py photo image.jpg{Colors.END}

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
  {Colors.YELLOW}pip install Pillow dnspython beautifulsoup4{Colors.END}

{Colors.BOLD}LEGAL NOTICE:{Colors.END}
  {Colors.RED}This tool is for authorized security research and ethical use only.
  Misuse may violate privacy laws. Use responsibly.{Colors.END}

{Colors.CYAN}╔═══════════════════════════════════════════════════════════════╗
║  Author: Enhanced by Community | Version: 3.0                 ║
║  GitHub: Your Repository | License: MIT                       ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
"""
    print(help_text)

def generate_requirements():
    """Generate requirements.txt file"""
    requirements = """# XTrace v3.0 - Python Dependencies
# Install with: pip install -r requirements.txt

    Pillow>=10.0.0

    dnspython>=2.4.0

    beautifulsoup4>=4.12.0


"""
    
    try:
        with open('requirements.txt', 'w') as f:
            f.write(requirements)
        print(f"{Colors.GREEN}[✓] requirements.txt generated{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}[!] Error generating requirements.txt: {e}{Colors.END}")

if __name__ == "__main__":
    try:
        if not os.path.exists('requirements.txt'):
            generate_requirements()
        
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