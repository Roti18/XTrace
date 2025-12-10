#!/bin/bash

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║          OSINT Tool - Setup Script                        ║"
echo "╚═══════════════════════════════════════════════════════════╝"

echo "[*] Membuat struktur folder..."
mkdir -p images results reports logs data/wordlists data/databases config modules utils tests docs

touch images/.gitkeep results/.gitkeep reports/.gitkeep logs/.gitkeep

echo "[*] Installing Python dependencies..."
pip3 install -r requirements.txt

chmod +x osint_tool.py

echo "[✓] Setup selesai!"
echo "[i] Jalankan: python3 osint_tool.py"