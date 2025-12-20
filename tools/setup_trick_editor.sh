#!/bin/bash
# Setup script for Trick Editor - Installs optional dependencies

echo "============================================"
echo "Trick Editor Setup"
echo "============================================"
echo ""
echo "This will install Pillow for GIF preview support."
echo ""
read -p "Press Enter to continue or Ctrl+C to cancel..."

echo ""
echo "Installing Pillow..."
python3 -m pip install --upgrade pip
python3 -m pip install Pillow

if [ $? -ne 0 ]; then
    echo ""
    echo "Error installing Pillow!"
    echo "Make sure Python 3 is installed."
    echo ""
    exit 1
fi

echo ""
echo "============================================"
echo "Installation complete!"
echo "============================================"
echo ""
echo "You can now run the Trick Editor with GIF preview support."
echo "Run ./run_trick_editor.sh to start editing."
echo ""

