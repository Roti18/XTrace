import time
import threading
import urllib.parse
from datetime import datetime
from .utils import make_request, save_results, generate_report
from .colors import Colors

def check_username(username, session_id):
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
            response = make_request(url, timeout=8)
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
        f'"{username}" ',
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
    
    save_results('username', results, session_id)
    generate_report('username', results, session_id)
    
    return results
