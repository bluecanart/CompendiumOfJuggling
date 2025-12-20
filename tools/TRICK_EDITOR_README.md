# Juggling Trick Editor - Python Application

A desktop application for editing the `tricks.json` file directly, replacing the web-based `trick-editor.html` that requires uploading and downloading files.

## Features

✨ **All the features from the HTML editor, plus:**

- 📂 **Direct File Access** - Opens and saves tricks.json directly without upload/download
- 🔍 **Real-time Search** - Filter tricks by name, slug, or siteswap
- ✏️ **Full Editing** - Edit all trick properties including:
  - Basic info (name, slug, category, difficulty, siteswap, etc.)
  - Description
  - Prerequisites and related tricks
  - Tags and trick families
  - Tutorial content (text and GIF sections)
  - Tutorial links
- ➕ **Create New Tricks** - Add new tricks to the collection
- 🗑️ **Delete Tricks** - Remove tricks with confirmation
- 📊 **Statistics** - View counts of tricks, learned status, families, and tags
- 💾 **Unsaved Changes Warning** - Warns before closing with unsaved work

## Installation

### Prerequisites

- Python 3.7 or higher
- tkinter (included with most Python installations)

### Setup

1. Navigate to the juggling-site directory:
   ```bash
   cd juggling-site
   ```

2. Run the editor:
   ```bash
   python trick_editor.py
   ```

   Or on some systems:
   ```bash
   python3 trick_editor.py
   ```

### Making it Executable (Optional)

**On Unix/Linux/macOS:**
```bash
chmod +x trick_editor.py
./trick_editor.py
```

**On Windows:**
- Right-click `trick_editor.py`
- Select "Open with" → "Python"
- Or create a shortcut with target: `python trick_editor.py`

## Usage

### Opening the File

The application automatically looks for `src/lib/data/tricks.json` when it starts. If found, it loads it automatically.

You can also:
1. Click "📂 Open JSON File" to browse for a different file
2. Edit the tricks as needed
3. Click "💾 Save Changes" to save directly to the file

### Editing Tricks

1. **Select a trick** from the list on the left
2. **Edit any fields** in the main editor area
3. **Click "💾 Save Changes"** to save the trick (this updates the in-memory data)
4. **Click "💾 Save Changes"** in the sidebar to write to the JSON file

### Creating New Tricks

1. Click "+ New Trick" button
2. Edit the fields as needed
3. Save changes

### Deleting Tricks

1. Select a trick
2. Click "🗑️ Delete" button
3. Confirm the deletion

### Searching

Type in the search box to filter tricks by:
- Trick name
- Slug (URL)
- Siteswap notation

## Keyboard Shortcuts

- `Ctrl+S` - Save file (when focused on editor)
- `Ctrl+F` - Focus search box
- Mouse wheel - Scroll through editor

## Troubleshooting

### "tkinter not found" Error

If you get an error about tkinter not being available:

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**Fedora:**
```bash
sudo dnf install python3-tkinter
```

**macOS:**
- Install Python from python.org (includes tkinter)
- Or use: `brew install python-tk`

**Windows:**
- Reinstall Python from python.org
- Make sure to check "tcl/tk and IDLE" in the installer

### File Not Loading

- Make sure you're in the `juggling-site` directory when running
- Or use "📂 Open JSON File" to manually select the tricks.json file

### Application Appears Blurry (Windows)

If the application appears blurry on high-DPI Windows displays:
- Right-click `trick_editor.py`
- Properties → Compatibility
- Click "Change high DPI settings"
- Check "Override high DPI scaling behavior"
- Select "System (Enhanced)"

## Differences from HTML Editor

**Advantages:**
- ✅ No need to upload/download files
- ✅ Direct file system access
- ✅ Auto-loads default tricks.json location
- ✅ Desktop application (no browser needed)
- ✅ Native file dialogs

**Trade-offs:**
- ⚠️ Requires Python installation
- ⚠️ Native desktop UI instead of web-based

## File Format

The application maintains complete compatibility with the original tricks.json format. All fields are preserved, including:

```json
{
  "id": "string",
  "name": "string",
  "slug": "string",
  "difficulty": number,
  "numBalls": number,
  "category": "string",
  "siteswap": "string",
  "prerequisites": ["string"],
  "relatedTricks": ["string"],
  "gifUrl": "string",
  "description": "string",
  "tutorialContent": [
    {"type": "text", "content": "string"},
    {"type": "gif", "url": "string"}
  ],
  "tutorialLinks": [
    {"title": "string", "url": "string"}
  ],
  "librarianLearned": boolean,
  "trickFamily": "string",
  "tags": ["string"]
}
```

## Support

For issues or questions, refer to the main juggling-site README or check the source code comments in `trick_editor.py`.

## License

This tool is part of the Compendium of Juggling project.

