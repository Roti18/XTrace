import socket
import ssl
import threading
from datetime import datetime
from .utils import make_request, save_results, generate_report
from .colors import Colors

try:
    import dns.resolver
    DNS_AVAILABLE = True
except ImportError:
    DNS_AVAILABLE = False

def check_domain(domain, session_id):
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
    else:
        print(f"\n{Colors.YELLOW}[!] dnspython not installed, skipping DNS record analysis.{Colors.END}")

    print(f"\n{Colors.BOLD}[*] Web Server Detection...{Colors.END}")
    for protocol in ['http', 'https']:
        url = f'{protocol}://{domain}'
        try:
            response = make_request(url, timeout=10)
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
    
    save_results('domain', results, session_id)
    generate_report('domain', results, session_id)
    
    return results
