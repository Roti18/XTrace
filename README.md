# XTrace | Advanced OSINT Intelligence Tool

Tool OSINT (Open Source Intelligence) canggih untuk investigasi digital yang legal dan etis.

## DISCLAIMER

Tool ini HANYA untuk penggunaan **LEGAL** dan **ETIS**:

- Security auditing dengan izin
- Investigasi digital yang sah
- Penelitian akademis
- Bug bounty programs

**DILARANG untuk**: stalking, harassment, atau aktivitas ilegal.

## Fitur

### 1. Username OSINT

- Cek keberadaan di 20+ platform
- Social media profiling
- Google Dorking otomatis

### 2. Email OSINT

- Validasi email
- Provider detection
- Breach checking (manual)
- MX records lookup

### 3. Domain OSINT

- WHOIS lookup
- DNS records
- Subdomain enumeration
- Web server analysis

### 4. IP Address OSINT

- Geolocation
- Reverse DNS
- Port scanning
- Network analysis

### 5. Phone Number OSINT

- Country detection
- Provider identification (Indonesia)
- Format validation
- WhatsApp checker

### 6. Social Media Profile OSINT

- Profile scraping
- Link extraction
- Email finding
- Contact discovery

### 7. Photo/Image OSINT

- EXIF metadata extraction
- GPS coordinates extraction
- Reverse image search
- File hash generation
- Camera info detection

## Instalasi

### Windows

```bash
# Clone repository
git clone https://github.com/Roti18/XTrace.git
cd XTrace

# Jalankan installer
install.bat
```

### Linux/maxOS

```bash
# Clone repository
git clone https://github.com/Roti18/XTrace.git
cd XTrace

# Berikan permission dan jalankan installer
chmod +x install.sh
./install.sh
```

## Cara Penggunaan

```bash
xtrace
```

### Contoh Penggunaan:

**1. Username Search:**

```
[?] Pilih opsi: 1
[?] Masukkan username: johndoe
```

**2. Photo Analysis:**

```
[?] Pilih opsi: 7
[?] Masukkan path foto: ./images/photo.jpg
```

**3. Export Results:**

```
[?] Pilih opsi: 10
[?] Nama file: hasil_investigasi.json
```

## Photo OSINT - Panduan Lengkap

### Apa yang Bisa Ditemukan?

1. **EXIF Metadata:**

   - Kamera yang digunakan
   - Tanggal & waktu pengambilan
   - Software editor
   - Copyright info

2. **GPS Coordinates:**

   - Lokasi foto diambil
   - Latitude & Longitude
   - Link ke Google Maps

3. **File Information:**
   - Hash untuk tracking
   - Dimensi & format
   - File size

### Contoh Output:

```
[*] Menganalisis foto: vacation.jpg
  [+] Nama file: vacation.jpg
  [+] Ukuran: 2458392 bytes (2400.78 KB)
  [+] Dimensi: 4032x3024
  [+] Format: JPEG

  [+] EXIF Data ditemukan:
      Make: Apple
      Model: iPhone 12 Pro
      DateTime: 2024:01:15 14:23:45
      Software: 15.2.1

  [+] GPS Data ditemukan!
      Latitude: -6.2088
      Longitude: 106.8456
      Google Maps: https://maps.google.com/?q=-6.2088,106.8456
```

### Tips Menggunakan Photo OSINT:

1. **Persiapan:**

   - Pastikan foto asli (bukan screenshot)
   - Hindari foto yang sudah di-upload ke social media (EXIF terhapus)
   - Gunakan foto original dari kamera/HP

2. **Analisis:**

   - Cek GPS coordinates untuk lokasi
   - Lihat timestamp untuk waktu
   - Identifikasi kamera untuk profiling

3. **Reverse Image Search:**
   - Upload ke Google Images, TinEye, Yandex
   - Cari foto serupa atau sumber asli
   - Gunakan PimEyes untuk facial recognition

## Struktur Project

```
osint-tool/
├── osint_tool.py          # Script utama
├── images/                # Simpan foto disini
├── results/               # Output JSON
└── requirements.txt       # Dependencies
```

## Legal & Ethics

### Yang BOLEH:

Investigasi dengan izin tertulis
Security research & bug bounty
Penelitian akademis
Self-assessment

### Yang TIDAK BOLEH:

Stalking atau harassment
Hacking tanpa izin
Privacy invasion
Illegal surveillance

## Privacy & Security

Tool ini:

- Hanya menggunakan data publik
- Tidak menyimpan data pribadi
- Tidak melakukan hacking
- Tidak bypass security

## Export Format

Results disimpan dalam JSON:

```json
{
  "timestamp": "2024-01-15T10:30:00",
  "username": {
    "query": "johndoe",
    "found": [...]
  },
  "photo": {
    "gps_decimal": {
      "latitude": -6.2088,
      "longitude": 106.8456
    }
  }
}
```

## License

MIT License - See LICENSE file

## Author

Created for educational and legal purposes only.

## Credits

- Python community
- OSINT Framework
- Pillow library
