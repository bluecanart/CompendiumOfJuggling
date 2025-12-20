#!/bin/bash
# Launcher for the Juggling Trick Editor
# Run this script to start the editor

cd "$(dirname "$0")"
python3 trick_editor.py

if [ $? -ne 0 ]; then
    echo ""
    echo "Error running the trick editor!"
    echo "Make sure Python 3 is installed."
    echo ""
    read -p "Press Enter to continue..."
fi

