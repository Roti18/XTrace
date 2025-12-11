import socket
import threading
from .utils import save_results, generate_report
from .colors import Colors

def check_ip(ip, session_id):
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
    
    save_results('ip', results, session_id)
    generate_report('ip', results, session_id)
    
    return results
