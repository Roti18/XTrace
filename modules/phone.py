import re
from .utils import save_results, generate_report
from .colors import Colors

def check_phone(phone, session_id):
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
    
    save_results('phone', results, session_id)
    generate_report('phone', results, session_id)
    
    return results
