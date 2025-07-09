#!/bin/bash

set -e

echo "Setting up Whisk..."

# Create Python virtual environment with system site packages
python3 -m venv venv --system-site-packages
source venv/bin/activate

# Install required Python package
pip install rapidfuzz

# Create .desktop file
DESKTOP_FILE=~/.local/share/applications/whisk.desktop
mkdir -p ~/.local/share/applications

cat > $DESKTOP_FILE <<EOL
[Desktop Entry]
Name=Whisk
Exec=$(pwd)/venv/bin/python3 $(pwd)/data/main.py
Icon=utilities-terminal
Type=Application
Categories=Utility;
EOL

echo ".desktop file created at $DESKTOP_FILE"

# Register GNOME shortcut (Alt+Space)
echo "Setting Alt+Space shortcut..."

SCHEMA='org.gnome.settings-daemon.plugins.media-keys'
KEY='custom-keybindings'
ENTRY='/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/whisk/'

# Register the shortcut path
gsettings set $SCHEMA $KEY "['$ENTRY']"

# Unregister Shortcut if taken
gsettings set org.gnome.desktop.wm.keybindings activate-window-menu "[]"

# Define shortcut metadata
gsettings set ${SCHEMA}.custom-keybinding:${ENTRY} name 'Whisk'
gsettings set ${SCHEMA}.custom-keybinding:${ENTRY} command "gtk-launch whisk"
gsettings set ${SCHEMA}.custom-keybinding:${ENTRY} binding '<Alt>space'

echo "Shortcut set to Alt+Space"

echo "Launching Whisk..."
python3 data/main.py
