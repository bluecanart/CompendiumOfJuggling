#!/usr/bin/env python3
"""
Juggling Trick Editor - A GUI application for editing tricks.json
Replaces the web-based trick-editor.html with direct file access
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
import copy
import urllib.request
import io

# Try to import PIL for better image handling
try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


class TrickEditor:
    """Main application for editing juggling tricks"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("🤹 Trick Editor - Compendium of Juggling")
        self.root.geometry("1400x900")
        
        # Data
        self.tricks: List[Dict[str, Any]] = []
        self.filtered_tricks: List[tuple] = []  # (index, trick)
        self.current_trick_index: Optional[int] = None
        self.file_path: Optional[Path] = None
        self.has_changes: bool = False
        
        # Find default tricks.json path
        default_path = Path(__file__).parent.parent / "src" / "lib" / "data" / "tricks.json"
        if default_path.exists():
            self.file_path = default_path
        
        # Setup UI
        self.setup_styles()
        self.create_ui()
        
        # Load file if found
        if self.file_path and self.file_path.exists():
            self.load_file(self.file_path)
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_styles(self):
        """Configure ttk styles for modern look"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colors inspired by the HTML version
        bg_primary = "#0f0f12"
        bg_secondary = "#17171c"
        bg_card = "#222229"
        text_primary = "#ffffff"
        text_secondary = "#a0a0b0"
        accent_yellow = "#ffd84d"
        accent_green = "#4dff88"
        
        # Configure styles
        style.configure("Sidebar.TFrame", background=bg_secondary)
        style.configure("Main.TFrame", background=bg_primary)
        style.configure("Card.TFrame", background=bg_card)
        style.configure("TLabel", background=bg_card, foreground=text_primary)
        style.configure("Title.TLabel", font=("Arial", 16, "bold"))
        style.configure("Section.TLabel", font=("Arial", 10, "bold"))
    
    def create_ui(self):
        """Create the main UI layout"""
        # Main container
        main_container = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Left sidebar
        self.create_sidebar(main_container)
        
        # Right main area
        self.create_main_area(main_container)
        
        main_container.add(self.sidebar_frame, weight=0)
        main_container.add(self.main_frame, weight=1)
    
    def create_sidebar(self, parent):
        """Create the left sidebar with trick list"""
        self.sidebar_frame = tk.Frame(parent, bg="#17171c", width=350)
        
        # Header
        header = tk.Frame(self.sidebar_frame, bg="#17171c")
        header.pack(fill=tk.X, padx=10, pady=10)
        
        title = tk.Label(header, text="🤹 Trick Editor", 
                        font=("Arial", 16, "bold"),
                        bg="#17171c", fg="#ffffff")
        title.pack(anchor=tk.W)
        
        subtitle = tk.Label(header, text="Compendium of Juggling",
                          font=("Arial", 9),
                          bg="#17171c", fg="#6b6b7a")
        subtitle.pack(anchor=tk.W)
        
        # File actions
        actions_frame = tk.Frame(self.sidebar_frame, bg="#17171c")
        actions_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.open_btn = tk.Button(actions_frame, text="📂 Open JSON File",
                                  command=self.open_file,
                                  bg="#222229", fg="#ffffff",
                                  relief=tk.FLAT, padx=15, pady=8,
                                  cursor="hand2")
        self.open_btn.pack(fill=tk.X, pady=2)
        
        self.save_btn = tk.Button(actions_frame, text="💾 Save Changes",
                                  command=self.save_file,
                                  bg="#4dff88", fg="#0f0f12",
                                  relief=tk.FLAT, padx=15, pady=8,
                                  font=("Arial", 9, "bold"),
                                  cursor="hand2", state=tk.DISABLED)
        self.save_btn.pack(fill=tk.X, pady=2)
        
        self.new_btn = tk.Button(actions_frame, text="+ New Trick",
                                command=self.create_new_trick,
                                bg="#222229", fg="#ffffff",
                                relief=tk.FLAT, padx=15, pady=8,
                                cursor="hand2", state=tk.DISABLED)
        self.new_btn.pack(fill=tk.X, pady=2)
        
        # Search box
        search_frame = tk.Frame(self.sidebar_frame, bg="#17171c")
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.search_var = tk.StringVar()
        
        search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                               bg="#222229", fg="#ffffff",
                               insertbackground="#ffffff",
                               relief=tk.FLAT, font=("Arial", 10))
        search_entry.pack(fill=tk.X, ipady=5)
        search_entry.insert(0, "Search tricks...")
        search_entry.bind('<FocusIn>', lambda e: search_entry.delete(0, tk.END) if search_entry.get() == "Search tricks..." else None)
        
        # Trick list
        list_frame = tk.Frame(self.sidebar_frame, bg="#17171c")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.trick_listbox = tk.Listbox(list_frame, 
                                        yscrollcommand=scrollbar.set,
                                        bg="#17171c", fg="#ffffff",
                                        selectbackground="#222229",
                                        selectforeground="#ffd84d",
                                        relief=tk.FLAT, font=("Arial", 10),
                                        highlightthickness=0,
                                        activestyle='none')
        self.trick_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.trick_listbox.yview)
        
        self.trick_listbox.bind('<<ListboxSelect>>', self.on_trick_select)
        
        # Now set up search callback after listbox is created
        self.search_var.trace('w', lambda *args: self.filter_tricks())
        
        # Stats
        self.stats_label = tk.Label(self.sidebar_frame,
                                    text="No tricks loaded",
                                    bg="#17171c", fg="#6b6b7a",
                                    font=("Arial", 9),
                                    justify=tk.LEFT)
        self.stats_label.pack(fill=tk.X, padx=10, pady=10)
    
    def create_main_area(self, parent):
        """Create the main editor area"""
        self.main_frame = tk.Frame(parent, bg="#0f0f12")
        
        # Create canvas for scrolling
        canvas = tk.Canvas(self.main_frame, bg="#0f0f12", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=canvas.yview)
        self.editor_frame = tk.Frame(canvas, bg="#0f0f12")
        
        self.editor_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.editor_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Initial message
        self.show_no_selection()
    
    def show_no_selection(self):
        """Show message when no trick is selected"""
        for widget in self.editor_frame.winfo_children():
            widget.destroy()
        
        container = tk.Frame(self.editor_frame, bg="#0f0f12")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        msg_frame = tk.Frame(container, bg="#0f0f12")
        msg_frame.pack(expand=True, fill=tk.BOTH)
        
        tk.Label(msg_frame, text="No trick selected",
                font=("Arial", 18, "bold"),
                bg="#0f0f12", fg="#6b6b7a").pack(anchor=tk.W, pady=(0, 10))
        
        tk.Label(msg_frame, text="Select a trick from the list or create a new one",
                font=("Arial", 11),
                bg="#0f0f12", fg="#6b6b7a").pack(anchor=tk.W)
    
    def create_editor(self, trick: Dict[str, Any]):
        """Create the editor form for a trick"""
        for widget in self.editor_frame.winfo_children():
            widget.destroy()
        
        container = tk.Frame(self.editor_frame, bg="#0f0f12")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(container, bg="#0f0f12")
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(header_frame, text=trick.get('name', 'Untitled'),
                font=("Arial", 20, "bold"),
                bg="#0f0f12", fg="#ffffff").pack(side=tk.LEFT)
        
        btn_frame = tk.Frame(header_frame, bg="#0f0f12")
        btn_frame.pack(side=tk.RIGHT)
        
        tk.Button(btn_frame, text="💾 Save Changes",
                 command=self.save_current_trick,
                 bg="#4dff88", fg="#0f0f12",
                 relief=tk.FLAT, padx=15, pady=8,
                 font=("Arial", 9, "bold"),
                 cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="🗑️ Delete",
                 command=self.delete_trick,
                 bg="#ff4d4d", fg="#ffffff",
                 relief=tk.FLAT, padx=15, pady=8,
                 cursor="hand2").pack(side=tk.LEFT)
        
        # Store references to form fields
        self.form_fields = {}
        
        # Basic Info Section
        self.create_section(container, "BASIC INFO")
        basic_grid = tk.Frame(container, bg="#17171c")
        basic_grid.pack(fill=tk.X, pady=(0, 15))
        
        self.create_field(basic_grid, "Name", trick.get('name', ''), 0, 0)
        self.create_field(basic_grid, "Slug (URL)", trick.get('slug', ''), 0, 1)
        
        self.create_category_field(basic_grid, trick.get('category', '3 Ball'), 1, 0)
        self.create_field(basic_grid, "Difficulty (1-10)", str(trick.get('difficulty', 5)), 1, 1, type='number')
        
        self.create_field(basic_grid, "Siteswap", trick.get('siteswap', ''), 2, 0)
        self.create_field(basic_grid, "GIF URL", trick.get('gifUrl', ''), 2, 1)
        
        self.create_field(basic_grid, "Trick Family", trick.get('trickFamily', ''), 3, 0)
        self.create_checkbox_field(basic_grid, "Librarian Learned", 
                                   trick.get('librarianLearned', False), 3, 1)
        
        # GIF Preview Section
        if trick.get('gifUrl', ''):
            self.create_section(container, "GIF PREVIEW")
            preview_frame = tk.Frame(container, bg="#17171c")
            preview_frame.pack(fill=tk.X, pady=(0, 15))
            self.create_gif_preview(preview_frame, trick.get('gifUrl', ''))
        
        # Description Section
        self.create_section(container, "DESCRIPTION")
        desc_frame = tk.Frame(container, bg="#17171c")
        desc_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.create_text_field(desc_frame, "description", trick.get('description', ''))
        
        # Prerequisites Section
        self.create_section(container, "PREREQUISITES")
        prereq_frame = tk.Frame(container, bg="#17171c")
        prereq_frame.pack(fill=tk.X, pady=(0, 15))
        self.create_array_field(prereq_frame, "prerequisites", trick.get('prerequisites', []))
        
        # Related Tricks Section
        self.create_section(container, "RELATED TRICKS")
        related_frame = tk.Frame(container, bg="#17171c")
        related_frame.pack(fill=tk.X, pady=(0, 15))
        self.create_array_field(related_frame, "relatedTricks", trick.get('relatedTricks', []))
        
        # Tags Section
        self.create_section(container, "TAGS")
        tags_frame = tk.Frame(container, bg="#17171c")
        tags_frame.pack(fill=tk.X, pady=(0, 15))
        self.create_array_field(tags_frame, "tags", trick.get('tags', []))
        
        # Tutorial Content Section
        self.create_section(container, "TUTORIAL CONTENT")
        content_frame = tk.Frame(container, bg="#17171c")
        content_frame.pack(fill=tk.X, pady=(0, 15))
        self.create_tutorial_content_field(content_frame, trick.get('tutorialContent', []))
        
        # Tutorial Links Section
        self.create_section(container, "TUTORIAL LINKS")
        links_frame = tk.Frame(container, bg="#17171c")
        links_frame.pack(fill=tk.X, pady=(0, 15))
        self.create_tutorial_links_field(links_frame, trick.get('tutorialLinks', []))
    
    def create_section(self, parent, title: str):
        """Create a section header"""
        frame = tk.Frame(parent, bg="#17171c")
        frame.pack(fill=tk.X, pady=(10, 5))
        
        tk.Label(frame, text=title,
                font=("Arial", 10, "bold"),
                bg="#17171c", fg="#6b6b7a").pack(anchor=tk.W, padx=15, pady=10)
    
    def create_field(self, parent, label: str, value: str, row: int, col: int, type='text'):
        """Create a form field"""
        frame = tk.Frame(parent, bg="#17171c")
        frame.grid(row=row, column=col, padx=10, pady=5, sticky="ew")
        parent.grid_columnconfigure(col, weight=1)
        
        tk.Label(frame, text=label, bg="#17171c", fg="#a0a0b0",
                font=("Arial", 9)).pack(anchor=tk.W, pady=(5, 2))
        
        if type == 'number':
            entry = tk.Spinbox(frame, from_=1, to=10, bg="#222229", fg="#ffffff",
                             relief=tk.FLAT, insertbackground="#ffffff")
            entry.delete(0, tk.END)
            entry.insert(0, value)
        else:
            entry = tk.Entry(frame, bg="#222229", fg="#ffffff",
                           relief=tk.FLAT, insertbackground="#ffffff")
            entry.insert(0, value)
        
        entry.pack(fill=tk.X, ipady=5)
        
        # Store field reference
        field_key = label.lower().replace(' ', '_').replace('_(url)', '').replace('_(1-10)', '')
        if field_key == 'slug_(url)' or field_key == 'slug':
            field_key = 'slug'
        elif field_key == 'gif_url':
            field_key = 'gifUrl'
        elif field_key == 'difficulty':
            field_key = 'difficulty'
        elif field_key == 'trick_family':
            field_key = 'trickFamily'
        
        self.form_fields[field_key] = entry
    
    def create_category_field(self, parent, value: str, row: int, col: int):
        """Create category dropdown"""
        frame = tk.Frame(parent, bg="#17171c")
        frame.grid(row=row, column=col, padx=10, pady=5, sticky="ew")
        
        tk.Label(frame, text="Category", bg="#17171c", fg="#a0a0b0",
                font=("Arial", 9)).pack(anchor=tk.W, pady=(5, 2))
        
        categories = ["2 Ball", "3 Ball", "4 Ball", "5 Ball", "6 Ball"]
        combo = ttk.Combobox(frame, values=categories, state='readonly')
        combo.set(value)
        combo.pack(fill=tk.X, ipady=5)
        
        self.form_fields['category'] = combo
    
    def create_checkbox_field(self, parent, label: str, value: bool, row: int, col: int):
        """Create a checkbox field"""
        frame = tk.Frame(parent, bg="#17171c")
        frame.grid(row=row, column=col, padx=10, pady=5, sticky="ew")
        
        var = tk.BooleanVar(value=value)
        cb = tk.Checkbutton(frame, text=label, variable=var,
                           bg="#17171c", fg="#a0a0b0",
                           selectcolor="#222229",
                           activebackground="#17171c",
                           activeforeground="#ffffff")
        cb.pack(anchor=tk.W, pady=10)
        
        self.form_fields['librarianLearned'] = var
    
    def create_text_field(self, parent, field_name: str, value: str):
        """Create a multi-line text field"""
        frame = tk.Frame(parent, bg="#17171c")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text = scrolledtext.ScrolledText(frame, height=8,
                                        bg="#222229", fg="#ffffff",
                                        insertbackground="#ffffff",
                                        relief=tk.FLAT)
        text.insert('1.0', value)
        text.pack(fill=tk.BOTH, expand=True)
        
        self.form_fields[field_name] = text
    
    def create_array_field(self, parent, field_name: str, values: List[str]):
        """Create an array editor"""
        frame = tk.Frame(parent, bg="#17171c")
        frame.pack(fill=tk.BOTH, padx=10, pady=10)
        
        # List to hold entry widgets
        entries = []
        
        def add_item():
            item_frame = tk.Frame(frame, bg="#17171c")
            item_frame.pack(fill=tk.X, pady=2)
            
            entry = tk.Entry(item_frame, bg="#222229", fg="#ffffff",
                           relief=tk.FLAT, insertbackground="#ffffff")
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
            entries.append(entry)
            
            def remove():
                entries.remove(entry)
                item_frame.destroy()
            
            tk.Button(item_frame, text="×", command=remove,
                     bg="#ff4d4d", fg="#ffffff",
                     relief=tk.FLAT, width=3,
                     cursor="hand2").pack(side=tk.RIGHT)
        
        # Add existing values
        for value in values:
            add_item()
            entries[-1].insert(0, value)
        
        # Add button
        tk.Button(frame, text=f"+ Add Item",
                 command=add_item,
                 bg="#222229", fg="#a0a0b0",
                 relief=tk.FLAT, cursor="hand2").pack(fill=tk.X, pady=(5, 0))
        
        self.form_fields[field_name] = entries
    
    def create_tutorial_content_field(self, parent, content: List[Dict]):
        """Create tutorial content editor"""
        frame = tk.Frame(parent, bg="#17171c")
        frame.pack(fill=tk.BOTH, padx=10, pady=10)
        
        content_items = []
        
        def add_content(content_type: str, initial_value: str = ""):
            item_frame = tk.Frame(frame, bg="#222229", relief=tk.FLAT, bd=1)
            item_frame.pack(fill=tk.X, pady=5, padx=5)
            
            header = tk.Frame(item_frame, bg="#222229")
            header.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(header, text=content_type.upper(),
                    bg="#222229", fg="#4d9fff",
                    font=("Arial", 8, "bold")).pack(side=tk.LEFT)
            
            def remove():
                content_items.remove((content_type, widget))
                item_frame.destroy()
            
            tk.Button(header, text="×", command=remove,
                     bg="#ff4d4d", fg="#ffffff",
                     relief=tk.FLAT, width=3,
                     cursor="hand2").pack(side=tk.RIGHT)
            
            if content_type == 'text':
                widget = scrolledtext.ScrolledText(item_frame, height=5,
                                                  bg="#2a2a33", fg="#ffffff",
                                                  insertbackground="#ffffff",
                                                  relief=tk.FLAT)
                widget.insert('1.0', initial_value)
                widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
            else:  # gif
                widget = tk.Entry(item_frame, bg="#2a2a33", fg="#ffffff",
                                relief=tk.FLAT, insertbackground="#ffffff")
                widget.insert(0, initial_value)
                widget.pack(fill=tk.X, padx=10, pady=(0, 10), ipady=5)
            
            content_items.append((content_type, widget))
        
        # Add existing content
        for item in content:
            if item['type'] == 'text':
                add_content('text', item.get('content', ''))
            else:
                add_content('gif', item.get('url', ''))
        
        # Add buttons
        btn_frame = tk.Frame(frame, bg="#17171c")
        btn_frame.pack(fill=tk.X, pady=(5, 0))
        
        tk.Button(btn_frame, text="+ Add Text",
                 command=lambda: add_content('text'),
                 bg="#222229", fg="#a0a0b0",
                 relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 2))
        
        tk.Button(btn_frame, text="+ Add GIF",
                 command=lambda: add_content('gif'),
                 bg="#222229", fg="#a0a0b0",
                 relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(2, 0))
        
        self.form_fields['tutorialContent'] = content_items
    
    def create_tutorial_links_field(self, parent, links: List[Dict]):
        """Create tutorial links editor"""
        frame = tk.Frame(parent, bg="#17171c")
        frame.pack(fill=tk.BOTH, padx=10, pady=10)
        
        link_items = []
        
        def add_link(title: str = "", url: str = ""):
            item_frame = tk.Frame(frame, bg="#222229", relief=tk.FLAT, bd=1)
            item_frame.pack(fill=tk.X, pady=5, padx=5)
            
            container = tk.Frame(item_frame, bg="#222229")
            container.pack(fill=tk.X, padx=10, pady=10)
            
            tk.Label(container, text="Title", bg="#222229", fg="#a0a0b0",
                    font=("Arial", 9)).pack(anchor=tk.W, pady=(0, 2))
            
            title_entry = tk.Entry(container, bg="#2a2a33", fg="#ffffff",
                                  relief=tk.FLAT, insertbackground="#ffffff")
            title_entry.insert(0, title)
            title_entry.pack(fill=tk.X, ipady=5, pady=(0, 5))
            
            tk.Label(container, text="URL", bg="#222229", fg="#a0a0b0",
                    font=("Arial", 9)).pack(anchor=tk.W, pady=(0, 2))
            
            url_entry = tk.Entry(container, bg="#2a2a33", fg="#ffffff",
                                relief=tk.FLAT, insertbackground="#ffffff")
            url_entry.insert(0, url)
            url_entry.pack(fill=tk.X, ipady=5, pady=(0, 5))
            
            def remove():
                link_items.remove((title_entry, url_entry))
                item_frame.destroy()
            
            tk.Button(container, text="× Remove Link", command=remove,
                     bg="#ff4d4d", fg="#ffffff",
                     relief=tk.FLAT, cursor="hand2").pack(anchor=tk.W, pady=(5, 0))
            
            link_items.append((title_entry, url_entry))
        
        # Add existing links
        for link in links:
            add_link(link.get('title', ''), link.get('url', ''))
        
        # Add button
        tk.Button(frame, text="+ Add Tutorial Link",
                 command=lambda: add_link(),
                 bg="#222229", fg="#a0a0b0",
                 relief=tk.FLAT, cursor="hand2").pack(fill=tk.X, pady=(5, 0))
        
        self.form_fields['tutorialLinks'] = link_items
    
    def create_gif_preview(self, parent, gif_url: str):
        """Create an animated GIF preview display"""
        frame = tk.Frame(parent, bg="#17171c")
        frame.pack(fill=tk.BOTH, padx=10, pady=10)
        
        preview_container = tk.Frame(frame, bg="#222229", relief=tk.FLAT)
        preview_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Try to load and display the GIF
        try:
            gif_path = None
            image_source = None
            
            # Check if it's a local path (relative to project)
            if not gif_url.startswith('http'):
                # The script is in tools/, GIFs are in static/
                script_dir = Path(__file__).parent  # tools/
                project_root = script_dir.parent     # juggling-site/
                
                # Try multiple locations
                potential_paths = [
                    # Most likely: static/ folder in project root
                    project_root / "static" / gif_url.lstrip('/'),
                    # Also try build/ folder
                    project_root / "build" / gif_url.lstrip('/'),
                    # Try relative to where tricks.json is
                    Path(self.file_path).parent.parent.parent / gif_url.lstrip('/'),
                    # Try absolute path
                    Path(gif_url)
                ]
                
                for path in potential_paths:
                    if path.exists():
                        gif_path = path
                        break
            
            if gif_path and gif_path.exists():
                # Load local file
                if HAS_PIL:
                    image_source = Image.open(gif_path)
                else:
                    # Fallback to tkinter PhotoImage (limited animation support)
                    photo = tk.PhotoImage(file=str(gif_path))
                    label = tk.Label(preview_container, image=photo, bg="#222229")
                    label.image = photo
                    label.pack(padx=10, pady=10)
                    return
                    
            elif gif_url.startswith('http'):
                # Try to load from URL
                if HAS_PIL:
                    req = urllib.request.Request(gif_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, timeout=5) as response:
                        image_data = response.read()
                    image_source = Image.open(io.BytesIO(image_data))
                else:
                    raise Exception("PIL required for URL images")
            else:
                raise FileNotFoundError("GIF file not found")
            
            # Animate the GIF if we have PIL and the image source
            if HAS_PIL and image_source:
                self._animate_gif(preview_container, image_source)
                
        except Exception as e:
            # Show error message or placeholder
            error_label = tk.Label(preview_container, 
                                  text=f"Unable to load GIF preview\n{gif_url}\n({str(e)[:50]}...)",
                                  bg="#222229", fg="#6b6b7a",
                                  font=("Arial", 9),
                                  wraplength=280,
                                  justify=tk.CENTER,
                                  padx=20, pady=20)
            error_label.pack()
    
    def _animate_gif(self, container, image_source):
        """Animate a GIF by cycling through its frames"""
        # Extract all frames
        frames = []
        durations = []
        
        try:
            while True:
                # Get current frame
                frame = image_source.copy()
                
                # Resize if too large
                max_size = (300, 300)
                frame.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # Convert to PhotoImage
                photo = ImageTk.PhotoImage(frame)
                frames.append(photo)
                
                # Get frame duration (default to 100ms if not specified)
                duration = image_source.info.get('duration', 100)
                durations.append(duration)
                
                # Move to next frame
                image_source.seek(image_source.tell() + 1)
                
        except EOFError:
            pass  # End of frames
        
        if not frames:
            return
        
        # Create label for animation
        label = tk.Label(container, bg="#222229")
        label.pack(padx=10, pady=10)
        
        # Animation state
        frame_index = [0]
        animation_id = [None]
        
        def update_frame():
            if not label.winfo_exists():
                return
            
            # Update to current frame
            label.config(image=frames[frame_index[0]])
            label.image = frames[frame_index[0]]
            
            # Move to next frame
            frame_index[0] = (frame_index[0] + 1) % len(frames)
            
            # Schedule next frame update
            delay = durations[frame_index[0]]
            animation_id[0] = label.after(delay, update_frame)
        
        # Start animation
        update_frame()
        
        # Store references to prevent garbage collection
        label._frames = frames
        label._animation_id = animation_id
    
    def load_file(self, path: Path):
        """Load tricks from JSON file"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.tricks = json.load(f)
            
            self.file_path = path
            self.filter_tricks()
            self.update_stats()
            self.save_btn.config(state=tk.NORMAL)
            self.new_btn.config(state=tk.NORMAL)
            
            # Update window title
            self.root.title(f"🤹 Trick Editor - {path.name}")
            
            self.show_toast(f"✓ Loaded {len(self.tricks)} tricks")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{e}")
    
    def open_file(self):
        """Open file dialog to select tricks.json"""
        path = filedialog.askopenfilename(
            title="Open tricks.json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialdir=Path(__file__).parent
        )
        
        if path:
            self.load_file(Path(path))
    
    def save_file(self):
        """Save tricks to JSON file"""
        if not self.file_path:
            messagebox.showerror("Error", "No file loaded")
            return
        
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.tricks, f, indent=2, ensure_ascii=False)
            
            self.has_changes = False
            self.show_toast(f"✓ Saved {len(self.tricks)} tricks to {self.file_path.name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{e}")
    
    def filter_tricks(self):
        """Filter tricks based on search term"""
        search_term = self.search_var.get().lower()
        if search_term == "search tricks...":
            search_term = ""
        
        self.filtered_tricks = []
        for i, trick in enumerate(self.tricks):
            name = trick.get('name', '').lower()
            slug = trick.get('slug', '').lower()
            siteswap = trick.get('siteswap', '').lower()
            
            if (search_term in name or search_term in slug or 
                search_term in siteswap or not search_term):
                self.filtered_tricks.append((i, trick))
        
        self.update_trick_list()
    
    def update_trick_list(self):
        """Update the trick listbox"""
        self.trick_listbox.delete(0, tk.END)
        
        for idx, trick in self.filtered_tricks:
            category = trick.get('category', '')
            difficulty = trick.get('difficulty', '')
            family = trick.get('trickFamily', '')
            learned = trick.get('librarianLearned', False)
            
            display = ""
            if learned:
                display += "✓C "
            display += f"{trick.get('name', 'Untitled')} "
            display += f"[{category}, Lvl {difficulty}]"
            if family:
                display += f" ({family})"
            
            self.trick_listbox.insert(tk.END, display)
    
    def on_trick_select(self, event):
        """Handle trick selection from list"""
        selection = self.trick_listbox.curselection()
        if not selection:
            return
        
        list_index = selection[0]
        actual_index, trick = self.filtered_tricks[list_index]
        
        self.current_trick_index = actual_index
        self.create_editor(trick)
    
    def save_current_trick(self):
        """Save the currently edited trick"""
        if self.current_trick_index is None:
            return
        
        trick = self.tricks[self.current_trick_index]
        
        try:
            # Basic fields
            trick['name'] = self.form_fields['name'].get()
            trick['slug'] = self.form_fields['slug'].get()
            trick['id'] = trick['slug']
            trick['category'] = self.form_fields['category'].get()
            trick['numBalls'] = int(trick['category'].split()[0])
            trick['difficulty'] = int(self.form_fields['difficulty'].get())
            trick['siteswap'] = self.form_fields['siteswap'].get()
            trick['gifUrl'] = self.form_fields['gifUrl'].get()
            trick['trickFamily'] = self.form_fields['trickFamily'].get()
            trick['librarianLearned'] = self.form_fields['librarianLearned'].get()
            
            # Description
            trick['description'] = self.form_fields['description'].get('1.0', 'end-1c')
            
            # Arrays
            trick['prerequisites'] = [e.get() for e in self.form_fields['prerequisites'] if e.get().strip()]
            trick['relatedTricks'] = [e.get() for e in self.form_fields['relatedTricks'] if e.get().strip()]
            trick['tags'] = [e.get() for e in self.form_fields['tags'] if e.get().strip()]
            
            # Tutorial content
            tutorial_content = []
            for content_type, widget in self.form_fields['tutorialContent']:
                if content_type == 'text':
                    content = widget.get('1.0', 'end-1c').strip()
                    if content:
                        tutorial_content.append({'type': 'text', 'content': content})
                else:  # gif
                    url = widget.get().strip()
                    if url:
                        tutorial_content.append({'type': 'gif', 'url': url})
            trick['tutorialContent'] = tutorial_content
            
            # Tutorial links
            tutorial_links = []
            for title_entry, url_entry in self.form_fields['tutorialLinks']:
                title = title_entry.get().strip()
                url = url_entry.get().strip()
                if title or url:
                    tutorial_links.append({'title': title, 'url': url})
            trick['tutorialLinks'] = tutorial_links
            
            self.has_changes = True
            self.filter_tricks()
            self.update_stats()
            
            self.show_toast("✓ Trick saved!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save trick:\n{e}")
    
    def delete_trick(self):
        """Delete the current trick"""
        if self.current_trick_index is None:
            return
        
        trick = self.tricks[self.current_trick_index]
        
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete '{trick.get('name', 'this trick')}'?"):
            del self.tricks[self.current_trick_index]
            self.current_trick_index = None
            self.has_changes = True
            
            self.filter_tricks()
            self.update_stats()
            self.show_no_selection()
            
            self.show_toast("✓ Trick deleted")
    
    def create_new_trick(self):
        """Create a new trick"""
        import time
        
        new_trick = {
            "id": f"new-trick-{int(time.time())}",
            "name": "New Trick",
            "slug": f"new-trick-{int(time.time())}",
            "difficulty": 5,
            "numBalls": 3,
            "category": "3 Ball",
            "siteswap": "",
            "prerequisites": [],
            "relatedTricks": [],
            "trickFamily": "",
            "tags": [],
            "gifUrl": "",
            "description": "",
            "tutorialContent": [],
            "tutorialLinks": [],
            "librarianLearned": False
        }
        
        self.tricks.append(new_trick)
        self.current_trick_index = len(self.tricks) - 1
        self.has_changes = True
        
        self.filter_tricks()
        self.update_stats()
        self.create_editor(new_trick)
        
        # Select the new trick in the list
        self.trick_listbox.selection_clear(0, tk.END)
        self.trick_listbox.selection_set(tk.END)
        self.trick_listbox.see(tk.END)
    
    def update_stats(self):
        """Update statistics display"""
        if not self.tricks:
            self.stats_label.config(text="No tricks loaded")
            return
        
        total = len(self.tricks)
        learned = sum(1 for t in self.tricks if t.get('librarianLearned', False))
        with_family = sum(1 for t in self.tricks if t.get('trickFamily', ''))
        with_tags = sum(1 for t in self.tricks if t.get('tags', []))
        
        stats_text = f"{total} tricks total\n"
        stats_text += f"{learned} marked as learned\n"
        stats_text += f"{with_family} with family\n"
        stats_text += f"{with_tags} with tags"
        
        self.stats_label.config(text=stats_text)
    
    def show_toast(self, message: str, duration: int = 2500):
        """Show a non-intrusive toast notification"""
        # Create toast window
        toast = tk.Toplevel(self.root)
        toast.overrideredirect(True)  # Remove window decorations
        toast.attributes('-topmost', True)  # Keep on top
        
        # Style the toast
        frame = tk.Frame(toast, bg="#222229", relief=tk.FLAT, bd=0)
        frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        # Add left border accent
        border = tk.Frame(frame, bg="#4dff88", width=4)
        border.pack(side=tk.LEFT, fill=tk.Y)
        
        # Message label
        label = tk.Label(frame, text=message,
                        bg="#222229", fg="#ffffff",
                        font=("Arial", 10),
                        padx=20, pady=12)
        label.pack(side=tk.LEFT)
        
        # Position at bottom right of main window
        toast.update_idletasks()
        toast_width = toast.winfo_width()
        toast_height = toast.winfo_height()
        
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()
        
        x = root_x + root_width - toast_width - 20
        y = root_y + root_height - toast_height - 60
        
        toast.geometry(f"+{x}+{y}")
        
        # Fade in effect (simplified - just show)
        toast.attributes('-alpha', 0.95)
        
        # Auto-close after duration
        def fade_out():
            try:
                toast.destroy()
            except:
                pass
        
        toast.after(duration, fade_out)
    
    def on_closing(self):
        """Handle window close event"""
        if self.has_changes:
            response = messagebox.askyesnocancel(
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save before closing?"
            )
            
            if response is None:  # Cancel
                return
            elif response:  # Yes
                self.save_file()
        
        self.root.destroy()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = TrickEditor(root)
    root.mainloop()


if __name__ == "__main__":
    main()

