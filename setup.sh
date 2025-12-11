#!/bin/bash

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║             XTrace - Final Installation Script            ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "This script will make the 'xtrace' command available system-wide"
echo "for the current user by doing the following:"
echo "1. Creating a standard directory at '~/.local/bin'."
echo "2. Placing a launcher script there."
echo "3. Ensuring that directory is in your PATH."
echo ""

read -p "Do you want to continue? (y/N): " choice
case "$choice" in 
  y|Y ) 
    # --- 1. Define and create the installation directory ---
    INSTALL_DIR="$HOME/.local/bin"
    echo ""
    echo "[*] Ensuring installation directory exists at $INSTALL_DIR..."
    mkdir -p "$INSTALL_DIR"
    echo "    Directory is present."

    # --- 2. Add the directory to the user's PATH if not already present ---
    # It's common for ~/.profile to handle this for ~/.local/bin, but we check/add just in case.
    echo ""
    echo "[*] Checking shell configuration for PATH..."
    SHELL_CONFIG_FILE=""
    if [ -n "$BASH_VERSION" ]; then
        SHELL_CONFIG_FILE="$HOME/.bashrc"
    elif [ -n "$ZSH_VERSION" ]; then
        SHELL_CONFIG_FILE="$HOME/.zshrc"
    else
        SHELL_CONFIG_FILE="$HOME/.profile"
    fi

    if ! grep -q 'export PATH="$HOME/.local/bin:$PATH"' "$SHELL_CONFIG_FILE"; then
        echo "    Adding ~/.local/bin to PATH in $SHELL_CONFIG_FILE..."
        echo '' >> "$SHELL_CONFIG_FILE"
        echo '# Add ~/.local/bin to PATH for user-installed executables' >> "$SHELL_CONFIG_FILE"
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_CONFIG_FILE"
        echo "    Configuration updated."
    else
        echo "    PATH configuration already present in $SHELL_CONFIG_FILE."
    fi

    # --- 3. Generate the launcher script ---
    echo ""
    echo "[*] Generating 'xtrace' launcher in the installation directory..."
    PROJECT_DIR="$(pwd)"
    LAUNCHER_PATH="$INSTALL_DIR/xtrace"
    
    cat > "$LAUNCHER_PATH" << EOF
#!/bin/bash
# This is an auto-generated launcher for XTrace. Do not edit.

PROJECT_DIR="$PROJECT_DIR"
VENV_DIR="\$PROJECT_DIR/.venv"
PYTHON_EXE="\$VENV_DIR/bin/python"

if [ ! -f "\$PYTHON_EXE" ]; then
    echo "[!] First-time setup for XTrace. This may take a moment..."
    echo "[*] Creating virtual environment in \$PROJECT_DIR..."
    if ! python3 -m venv "\$VENV_DIR"; then
        echo "[!] ERROR: Failed to create virtual environment."
        exit 1
    fi

    echo "[*] Installing dependencies..."
    if ! "\$PYTHON_EXE" -m pip install -e "\$PROJECT_DIR"; then
        echo "[!] ERROR: Failed to install dependencies."
        exit 1
    fi
    echo "[✓] Setup complete!"
fi

"\$PYTHON_EXE" "\$PROJECT_DIR/xtrace.py" "\$@"
EOF

    chmod +x "$LAUNCHER_PATH"
    echo "    Launcher created."

    echo ""
    echo "╔═════════════════════════════════════════════════════════════════════════════╗"
    echo "║ [✓] Installation Complete!                                                ║"
    echo "║                                                                             ║"
    echo "║ IMPORTANT: You must CLOSE and REOPEN your terminal for the 'xtrace' command ║"
    echo "║ to be available everywhere.                                                 ║"
    echo "║                                                                             ║"
    echo "║ You may need to run 'source $SHELL_CONFIG_FILE' in your current terminal.     ║"
    echo "╚═════════════════════════════════════════════════════════════════════════════╝"
    echo ""
    ;;
  * )
    echo ""
    echo "Installation cancelled by user."
    echo ""
    ;;
esac
