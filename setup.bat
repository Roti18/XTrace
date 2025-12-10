@echo off
echo ╔═══════════════════════════════════════════════════════════╗
echo ║          OSINT Tool - Setup Script                        ║
echo ╚═══════════════════════════════════════════════════════════╝

echo [*] Membuat struktur folder...
mkdir images results reports logs data\wordlists data\databases config modules utils tests docs

echo [*] Installing Python dependencies...
pip install -r requirements.txt

echo [✓] Setup selesai!
echo [i] Jalankan: python osint_tool.py
pause