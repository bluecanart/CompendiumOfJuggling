# Quick Start Guide - Juggling Trick Editor

## 🚀 Getting Started in 30 Seconds

### Windows Users

1. **Double-click** `run_trick_editor.bat` in the `juggling-site` folder
2. The app opens automatically with your tricks loaded
3. Start editing!

### Mac/Linux Users

1. **Run in terminal:**
   ```bash
   cd juggling-site
   ./run_trick_editor.sh
   ```
   Or:
   ```bash
   python3 trick_editor.py
   ```
2. The app opens automatically with your tricks loaded
3. Start editing!

---

## 🎨 Optional: Enable GIF Previews

To see trick animations directly in the editor:

```bash
pip install Pillow
```

Then restart the app! GIFs will automatically appear when you select a trick.

---

## 📝 Common Tasks

### Edit a Trick

1. Click on any trick in the left sidebar
2. View the GIF preview (if available)
3. Modify the fields you want
4. Click **💾 Save Changes** (top right)
5. Click **💾 Save Changes** (sidebar) to save to file

### Create a New Trick

1. Click **+ New Trick** button (sidebar)
2. Fill in the details
3. Click **💾 Save Changes** (top right)
4. Click **💾 Save Changes** (sidebar) to save to file

### Delete a Trick

1. Select the trick you want to delete
2. Click **🗑️ Delete** button (top right)
3. Confirm the deletion
4. Click **💾 Save Changes** (sidebar) to save to file

### Search for Tricks

- Type in the search box at the top of the sidebar
- Filters by name, slug, or siteswap
- Updates instantly as you type

---

## 💡 Tips

- **Always save twice**: Once to save the trick (top button), once to save to file (sidebar button)
- **Watch for toast notifications**: Success messages appear briefly in the bottom-right corner
- **GIF previews**: Install Pillow to see trick animations in the editor
- **Search while editing**: You can search and switch between tricks without losing changes
- **Unsaved warning**: The app will warn you if you try to close with unsaved changes
- **Statistics**: Check the bottom of the sidebar for trick counts and stats
- **Learned badge**: Tricks you've learned show "✓C" at the start of their name

---

## ❓ Troubleshooting

**App won't start?**
- Make sure Python 3.7+ is installed
- On Windows: Download from [python.org](https://www.python.org/downloads/)
- On Mac: Comes pre-installed or use Homebrew
- On Linux: `sudo apt-get install python3 python3-tk`

**No GIF previews?**
- Install Pillow: `pip install Pillow`
- Check that GIF URLs are correct
- Restart the app after installing Pillow

**Changes not saving?**
- Remember to click **💾 Save Changes** in the sidebar after editing tricks
- Check that `tricks.json` is not read-only

**Need more help?**
- See `TRICK_EDITOR_README.md` for full documentation
- Check the main project README

---

## 🎯 What's Different from the HTML Editor?

| Feature | HTML Editor | Python App |
|---------|-------------|------------|
| File Upload/Download | ❌ Required | ✅ Direct access |
| Auto-loads tricks.json | ❌ Manual | ✅ Automatic |
| GIF Previews | ❌ No | ✅ Yes (with Pillow) |
| Toast Notifications | ❌ No | ✅ Yes |
| Works offline | ✅ Yes | ✅ Yes |
| Requires Python | ❌ No | ✅ Yes |
| Native app feel | ❌ Browser | ✅ Desktop |

---

**That's it! You're ready to edit tricks efficiently! 🤹**

🎁 **Pro Tip**: Install Pillow for the best experience with GIF previews!

