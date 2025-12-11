import os
import json
from datetime import datetime
import urllib.request
import urllib.parse
import urllib.error
import socket
import ssl
from .colors import Colors

# SSL context and headers for requests
ssl_context = ssl._create_unverified_context()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

def ensure_directories():
    """Pastikan semua folder yang dibutuhkan ada"""
    dirs = ['docs', 'images', 'logs', 'result', 'reports', 'data']
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)

def log(message, level="INFO"):
    """Logging ke file dengan format lengkap"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file = f"logs/xtrace_{datetime.now().strftime('%Y%m%d')}.log"
    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] [{level}] {message}\n")
    except:
        pass

def make_request(url, timeout=10, method='GET', data=None):
    """HTTP request dengan error handling lengkap"""
    try:
        if data:
            data = urllib.parse.urlencode(data).encode('utf-8')
        
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        response = urllib.request.urlopen(req, timeout=timeout, context=ssl_context)
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
        log(f"Request error for {url}: {str(e)}", "ERROR")
        return None

def save_results(mode, data, session_id):
    """Simpan hasil ke file JSON dengan format lengkap"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"result/{mode}_{timestamp}.json"
    
    result_data = {
        'session_id': session_id,
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
        log(f"Results saved: {filename}")
        return filename
    except Exception as e:
        print(f"{Colors.RED}[!] Error saving results: {e}{Colors.END}")
        return None

def generate_report(mode, data, session_id):
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
        <p>Mode: {mode.upper()} | Session: {session_id}</p>
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
