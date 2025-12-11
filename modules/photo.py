import os
import hashlib
from .utils import save_results, generate_report
from .colors import Colors

try:
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

def check_photo(photo_path, session_id):
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
        
        save_results('photo', results, session_id)
        generate_report('photo', results, session_id)
        
        return results
        
    except Exception as e:
        print(f"{Colors.RED}[!] Error analyzing photo: {e}{Colors.END}")
        return None
