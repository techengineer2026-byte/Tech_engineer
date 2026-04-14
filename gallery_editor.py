import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import json
import os
import threading
import http.server
import socketserver
from pathlib import Path

class GalleryJSONEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("🎨 Tech Engineer Gallery JSON Editor")
        self.root.geometry("1600x900")
        self.root.configure(bg="#f5f5f5")
        
        # Data
        self.json_path = None
        self.auto_save_enabled = tk.BooleanVar(value=True)
        self.auto_save_interval = 10000  # 10 seconds
        self.unsaved_changes = False
        
        self.data = {
            "galleries": [],
            "layouts": {
                "tall": {"colClass": "col-md-4", "defaultHeight": 500},
                "wide": {"colClass": "col-md-4", "defaultHeight": 250},
                "square": {"colClass": "col-md-5", "defaultHeight": 400},
                "narrow": {"colClass": "col-md-3", "defaultHeight": 400},
                "medium": {"colClass": "col-md-4", "defaultHeight": 400},
                "grid": {"colClass": "col-6 col-md-3", "defaultHeight": 200},
                "hero": {"colClass": "col-12", "defaultHeight": 450}
            }
        }
        self.current_gallery_index = None
        self.current_image_index = None
        
        # Local server
        self.server = None
        self.server_port = 8000
        self.server_running = False
        
        self.setup_ui()
        self.auto_load_json()
        self.start_auto_save()
        
    def setup_ui(self):
        # Menu Bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # FILE MENU
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="📁 File", menu=file_menu)
        file_menu.add_command(label="Open gallery.json", command=self.open_json, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_json, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.save_json_as)
        file_menu.add_separator()
        file_menu.add_checkbutton(label="Auto-Save (Every 10s)", variable=self.auto_save_enabled)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        
        # SERVER MENU
        server_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="🌐 Server", menu=server_menu)
        server_menu.add_command(label="Start Local Server", command=self.start_server)
        server_menu.add_command(label="Stop Local Server", command=self.stop_server)
        server_menu.add_command(label="Open in Browser", command=self.open_in_browser)
        
        # HELP MENU
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="❓ Help", menu=help_menu)
        help_menu.add_command(label="Quick Start Guide", command=self.show_guide)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Status Bar at Top
        self.status_bar = tk.Frame(self.root, bg="#3f51b5", height=40)
        self.status_bar.pack(fill=tk.X, side=tk.TOP)
        
        self.status_label = tk.Label(
            self.status_bar, 
            text="No file loaded - Click 'File > Open gallery.json' or create new",
            fg="white", 
            bg="#3f51b5",
            font=("Segoe UI", 10),
            anchor='w',
            padx=15
        )
        self.status_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.server_status = tk.Label(
            self.status_bar,
            text="🔴 Server: Offline",
            fg="white",
            bg="#3f51b5",
            font=("Segoe UI", 10, "bold"),
            padx=15
        )
        self.server_status.pack(side=tk.RIGHT)
        
        # Main Container
        main_paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, bg="#f5f5f5", sashwidth=5)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # LEFT PANEL - Gallery List
        left_frame = tk.Frame(main_paned, bg="white", width=320, relief=tk.RAISED, borderwidth=1)
        main_paned.add(left_frame)
        
        tk.Label(left_frame, text="📚 Gallery Sections", font=("Segoe UI", 16, "bold"), 
                bg="#3f51b5", fg="white", pady=15).pack(fill=tk.X)
        
        # Gallery Listbox
        list_frame = tk.Frame(left_frame, bg="white")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.gallery_listbox = tk.Listbox(
            list_frame, 
            yscrollcommand=scrollbar.set,
            font=("Segoe UI", 11),
            selectmode=tk.SINGLE,
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground="#3f51b5"
        )
        self.gallery_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.gallery_listbox.yview)
        self.gallery_listbox.bind('<<ListboxSelect>>', self.on_gallery_select)
        
        # Gallery Controls
        btn_frame = tk.Frame(left_frame, bg="white")
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(btn_frame, text="➕ Add Gallery", command=self.add_gallery,
                 bg="#4CAF50", fg="white", font=("Segoe UI", 10, "bold"), 
                 cursor="hand2", relief=tk.FLAT, pady=8).pack(fill=tk.X, pady=3)
        tk.Button(btn_frame, text="✏️ Edit Gallery", command=self.edit_gallery,
                 bg="#2196F3", fg="white", font=("Segoe UI", 10, "bold"),
                 cursor="hand2", relief=tk.FLAT, pady=8).pack(fill=tk.X, pady=3)
        tk.Button(btn_frame, text="🗑️ Delete Gallery", command=self.delete_gallery,
                 bg="#f44336", fg="white", font=("Segoe UI", 10, "bold"),
                 cursor="hand2", relief=tk.FLAT, pady=8).pack(fill=tk.X, pady=3)
        
        # CENTER PANEL - Image Grid
        center_frame = tk.Frame(main_paned, bg="white", relief=tk.RAISED, borderwidth=1)
        main_paned.add(center_frame)
        
        # Gallery Info Header
        self.gallery_info = tk.Label(
            center_frame, 
            text="Select a gallery section from the left", 
            font=("Segoe UI", 13, "bold"), 
            bg="#3f51b5", 
            fg="white", 
            pady=15
        )
        self.gallery_info.pack(fill=tk.X)
        
        # Canvas for scrolling
        canvas_frame = tk.Frame(center_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        canvas_scroll_y = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL)
        canvas_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.images_canvas = tk.Canvas(
            canvas_frame, 
            bg="#fafafa",
            yscrollcommand=canvas_scroll_y.set
        )
        self.images_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canvas_scroll_y.config(command=self.images_canvas.yview)
        
        self.images_frame = tk.Frame(self.images_canvas, bg="#fafafa")
        self.images_canvas.create_window((0, 0), window=self.images_frame, anchor='nw')
        self.images_frame.bind('<Configure>', 
                              lambda e: self.images_canvas.configure(
                                  scrollregion=self.images_canvas.bbox('all')))
        
        # Image Control Buttons
        img_btn_frame = tk.Frame(center_frame, bg="white")
        img_btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(img_btn_frame, text="➕ Add Image", command=self.add_image,
                 bg="#4CAF50", fg="white", font=("Segoe UI", 10, "bold"),
                 cursor="hand2", relief=tk.FLAT, padx=15, pady=8).pack(side=tk.LEFT, padx=5)
        tk.Button(img_btn_frame, text="⬆️ Move Up", command=lambda: self.move_image(-1),
                 bg="#FF9800", fg="white", font=("Segoe UI", 10, "bold"),
                 cursor="hand2", relief=tk.FLAT, padx=15, pady=8).pack(side=tk.LEFT, padx=5)
        tk.Button(img_btn_frame, text="⬇️ Move Down", command=lambda: self.move_image(1),
                 bg="#FF9800", fg="white", font=("Segoe UI", 10, "bold"),
                 cursor="hand2", relief=tk.FLAT, padx=15, pady=8).pack(side=tk.LEFT, padx=5)
        
        # RIGHT PANEL - Properties Editor
        right_frame = tk.Frame(main_paned, bg="white", width=380, relief=tk.RAISED, borderwidth=1)
        main_paned.add(right_frame)
        
        tk.Label(right_frame, text="🖼️ Image Properties", font=("Segoe UI", 16, "bold"),
                bg="#3f51b5", fg="white", pady=15).pack(fill=tk.X)
        
        # Image Preview
        preview_frame = tk.Frame(right_frame, bg="#e0e0e0", relief=tk.SUNKEN, borderwidth=2)
        preview_frame.pack(pady=15, padx=15)
        
        self.preview_label = tk.Label(
            preview_frame, 
            text="No image selected\n\nClick 'Edit' on an image", 
            bg="#e0e0e0",
            font=("Segoe UI", 10),
            width=35,
            height=12
        )
        self.preview_label.pack(padx=5, pady=5)
        
        # Properties Form
        props_container = tk.Frame(right_frame, bg="white")
        props_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Scrollable frame for properties
        canvas = tk.Canvas(props_container, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(props_container, orient="vertical", command=canvas.yview)
        props_frame = tk.Frame(canvas, bg="white")
        
        props_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=props_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Source
        tk.Label(props_frame, text="📂 Image Source Path:", bg="white", 
                font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky='w', pady=8, padx=5)
        
        src_frame = tk.Frame(props_frame, bg="white")
        src_frame.grid(row=1, column=0, sticky='ew', padx=5)
        props_frame.columnconfigure(0, weight=1)
        
        self.src_entry = tk.Entry(src_frame, font=("Segoe UI", 9), relief=tk.SOLID, borderwidth=1)
        self.src_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.src_entry.bind('<KeyRelease>', lambda e: self.mark_unsaved())
        
        tk.Button(src_frame, text="📁", command=self.browse_image,
                 bg="#607D8B", fg="white", font=("Segoe UI", 9, "bold"),
                 cursor="hand2", relief=tk.FLAT).pack(side=tk.RIGHT, padx=5)
        
        # Alt Text
        tk.Label(props_frame, text="🏷️ Alt Text (SEO Description):", bg="white",
                font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky='w', pady=(15,5), padx=5)
        
        self.alt_text = tk.Text(props_frame, width=40, height=4, wrap=tk.WORD, 
                               font=("Segoe UI", 9), relief=tk.SOLID, borderwidth=1)
        self.alt_text.grid(row=3, column=0, pady=5, padx=5, sticky='ew')
        self.alt_text.bind('<KeyRelease>', lambda e: self.mark_unsaved())
        
        # Layout Type
        tk.Label(props_frame, text="📐 Layout Type:", bg="white",
                font=("Segoe UI", 10, "bold")).grid(row=4, column=0, sticky='w', pady=(15,5), padx=5)
        
        self.layout_var = tk.StringVar()
        self.layout_var.trace('w', lambda *args: self.mark_unsaved())
        
        layout_combo = ttk.Combobox(
            props_frame, 
            textvariable=self.layout_var,
            values=["tall", "wide", "square", "narrow", "medium", "grid", "hero"],
            state="readonly",
            font=("Segoe UI", 9),
            width=37
        )
        layout_combo.grid(row=5, column=0, pady=5, padx=5, sticky='ew')
        
        # Height
        tk.Label(props_frame, text="📏 Height (pixels):", bg="white",
                font=("Segoe UI", 10, "bold")).grid(row=6, column=0, sticky='w', pady=(15,5), padx=5)
        
        self.height_entry = tk.Entry(props_frame, font=("Segoe UI", 9), relief=tk.SOLID, borderwidth=1)
        self.height_entry.grid(row=7, column=0, sticky='ew', pady=5, padx=5)
        self.height_entry.bind('<KeyRelease>', lambda e: self.mark_unsaved())
        
        # Action Buttons
        tk.Button(props_frame, text="💾 Update Image", command=self.update_image,
                 bg="#2196F3", fg="white", font=("Segoe UI", 11, "bold"),
                 cursor="hand2", relief=tk.FLAT, pady=10).grid(row=8, column=0, sticky='ew', pady=15, padx=5)
        
        tk.Button(props_frame, text="🗑️ Delete This Image", command=self.delete_image,
                 bg="#f44336", fg="white", font=("Segoe UI", 11, "bold"),
                 cursor="hand2", relief=tk.FLAT, pady=10).grid(row=9, column=0, sticky='ew', pady=5, padx=5)
        
        # Quick Presets
        tk.Label(props_frame, text="⚡ Quick Layout Presets:", bg="white",
                font=("Segoe UI", 10, "bold")).grid(row=10, column=0, sticky='w', pady=(20,10), padx=5)
        
        presets = [
            ("📏 Tall Portrait (500px)", "tall", 500),
            ("📐 Wide Landscape (250px)", "wide", 250),
            ("⬜ Square (400px)", "square", 400),
            ("📱 Small Grid (200px)", "grid", 200),
            ("🖼️ Hero Banner (450px)", "hero", 450)
        ]
        
        for i, (text, layout, height) in enumerate(presets):
            tk.Button(
                props_frame, 
                text=text,
                command=lambda l=layout, h=height: self.apply_preset(l, h),
                bg="#607D8B", fg="white", font=("Segoe UI", 9),
                cursor="hand2", relief=tk.FLAT, pady=6
            ).grid(row=11+i, column=0, sticky='ew', pady=3, padx=5)
        
        # Keyboard Shortcuts
        self.root.bind('<Control-o>', lambda e: self.open_json())
        self.root.bind('<Control-s>', lambda e: self.save_json())
        
        # Window close protocol
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    # ═══════════════════════════════════════════════════════
    # AUTO-LOAD & AUTO-SAVE FUNCTIONALITY
    # ═══════════════════════════════════════════════════════
    
    def auto_load_json(self):
        """Automatically load gallery.json if it exists in current directory"""
        default_path = os.path.join(os.getcwd(), "gallery.json")
        
        if os.path.exists(default_path):
            self.json_path = default_path
            try:
                with open(default_path, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                    
                if "layouts" not in loaded_data:
                    loaded_data["layouts"] = self.data["layouts"]
                
                self.data = loaded_data
                self.refresh_gallery_list()
                self.update_status(f"✅ Auto-loaded: {default_path}")
            except Exception as e:
                self.update_status(f"⚠️ Error loading gallery.json: {str(e)}")
        else:
            self.update_status("No gallery.json found. Create one using File > Save As")
    
    def mark_unsaved(self):
        """Mark that there are unsaved changes"""
        if not self.unsaved_changes:
            self.unsaved_changes = True
            if self.json_path:
                title = self.root.title()
                if not title.endswith("*"):
                    self.root.title(title + " *")
    
    def start_auto_save(self):
        """Start auto-save timer"""
        if self.auto_save_enabled.get() and self.json_path and self.unsaved_changes:
            self.save_json(silent=True)
        
        # Schedule next auto-save
        self.root.after(self.auto_save_interval, self.start_auto_save)
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_label.config(text=message)
    
    # ═══════════════════════════════════════════════════════
    # LOCAL SERVER FUNCTIONALITY
    # ═══════════════════════════════════════════════════════
    
    def start_server(self):
        """Start local HTTP server to serve gallery.json"""
        if self.server_running:
            messagebox.showinfo("Server Running", f"Server already running at http://localhost:{self.server_port}")
            return
        
        try:
            # Change to directory containing gallery.json
            if self.json_path:
                os.chdir(os.path.dirname(self.json_path))
            
            # Create server
            Handler = http.server.SimpleHTTPRequestHandler
            self.server = socketserver.TCPServer(("", self.server_port), Handler)
            
            # Run in separate thread
            server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
            server_thread.start()
            
            self.server_running = True
            self.server_status.config(text=f"🟢 Server: http://localhost:{self.server_port}")
            
            messagebox.showinfo(
                "Server Started ✓", 
                f"Local server running at:\nhttp://localhost:{self.server_port}\n\n"
                f"Open gallery.html in your browser to test.\n"
                f"The gallery.json will be fetched from:\nhttp://localhost:{self.server_port}/gallery.json"
            )
        except Exception as e:
            messagebox.showerror("Server Error", f"Failed to start server:\n{str(e)}")
    
    def stop_server(self):
        """Stop local HTTP server"""
        if not self.server_running:
            messagebox.showinfo("Server Not Running", "No server is currently running.")
            return
        
        try:
            self.server.shutdown()
            self.server = None
            self.server_running = False
            self.server_status.config(text="🔴 Server: Offline")
            messagebox.showinfo("Server Stopped", "Local server has been stopped.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop server:\n{str(e)}")
    
    def open_in_browser(self):
        """Open gallery.html in default browser"""
        if not self.server_running:
            response = messagebox.askyesno(
                "Server Not Running",
                "Local server is not running. Start it now?"
            )
            if response:
                self.start_server()
            else:
                return
        
        # Find gallery.html
        gallery_html = os.path.join(os.path.dirname(self.json_path or os.getcwd()), "gallery.html")
        
        if os.path.exists(gallery_html):
            import webbrowser
            webbrowser.open(f"http://localhost:{self.server_port}/gallery.html")
        else:
            messagebox.showwarning(
                "File Not Found",
                f"gallery.html not found in:\n{os.path.dirname(self.json_path or os.getcwd())}\n\n"
                f"Make sure gallery.html is in the same directory as gallery.json"
            )
    
    # ═══════════════════════════════════════════════════════
    # FILE OPERATIONS
    # ═══════════════════════════════════════════════════════
    
    def open_json(self):
        filename = filedialog.askopenfilename(
            title="Open Gallery JSON",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile="gallery.json"
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                    
                if "layouts" not in loaded_data:
                    loaded_data["layouts"] = self.data["layouts"]
                
                self.data = loaded_data
                self.json_path = filename
                self.unsaved_changes = False
                self.refresh_gallery_list()
                self.update_status(f"✅ Loaded: {filename}")
                self.root.title(f"🎨 Gallery Editor - {os.path.basename(filename)}")
                messagebox.showinfo("Success ✓", f"Loaded gallery.json\n{len(self.data.get('galleries', []))} galleries found!")
            except Exception as e:
                messagebox.showerror("Error ✗", f"Failed to load JSON:\n{str(e)}")
    
    def save_json(self, silent=False):
        """Save JSON file
        Args:
            silent (bool): If True, don't show success message (for auto-save)
        """
        if not self.json_path:
            self.save_json_as()
            return
        
        try:
            with open(self.json_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            
            self.unsaved_changes = False
            title = self.root.title().replace(" *", "")
            self.root.title(title)
            
            if not silent:
                self.update_status(f"💾 Saved: {self.json_path}")
                messagebox.showinfo("Saved ✓", f"Successfully saved to:\n{self.json_path}")
            else:
                self.update_status(f"🔄 Auto-saved at {self.get_time()}")
        except Exception as e:
            messagebox.showerror("Error ✗", f"Failed to save:\n{str(e)}")
    
    def save_json_as(self):
        filename = filedialog.asksaveasfilename(
            title="Save Gallery JSON As",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialfile="gallery.json"
        )
        if filename:
            self.json_path = filename
            self.save_json()
            self.root.title(f"🎨 Gallery Editor - {os.path.basename(filename)}")
    
    def get_time(self):
        """Get current time as string"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")
    
    def on_closing(self):
        """Handle window close event"""
        if self.unsaved_changes:
            response = messagebox.askyesnocancel(
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save before closing?"
            )
            if response is None:  # Cancel
                return
            elif response:  # Yes
                self.save_json()
        
        # Stop server if running
        if self.server_running:
            self.stop_server()
        
        self.root.destroy()
    
    # ═══════════════════════════════════════════════════════
    # EXISTING METHODS (Keep all your previous methods here)
    # ═══════════════════════════════════════════════════════
    
    def refresh_gallery_list(self):
        self.gallery_listbox.delete(0, tk.END)
        for gallery in self.data.get("galleries", []):
            display_text = f"📁 {gallery.get('title', 'Untitled')} ({len(gallery.get('images', []))} images)"
            self.gallery_listbox.insert(tk.END, display_text)
    
    def on_gallery_select(self, event):
        selection = self.gallery_listbox.curselection()
        if selection:
            self.current_gallery_index = selection[0]
            self.current_image_index = None
            self.display_gallery_images()
    
    def display_gallery_images(self):
        for widget in self.images_frame.winfo_children():
            widget.destroy()
        
        if self.current_gallery_index is None:
            return
        
        gallery = self.data["galleries"][self.current_gallery_index]
        self.gallery_info.config(
            text=f"📸 {gallery.get('title', 'Untitled')} - {len(gallery.get('images', []))} images"
        )
        
        images = gallery.get("images", [])
        
        for i, img_data in enumerate(images):
            frame = tk.Frame(self.images_frame, bg="white", relief=tk.RAISED, borderwidth=2)
            frame.grid(row=i//3, column=i%3, padx=12, pady=12, sticky='nsew')
            
            try:
                img_path = img_data.get("src", "")
                if img_path.startswith('/'):
                    img_path = img_path[1:]
                
                if os.path.exists(img_path):
                    img = Image.open(img_path)
                    img.thumbnail((180, 180))
                    photo = ImageTk.PhotoImage(img)
                    label = tk.Label(frame, image=photo, bg="white")
                    label.image = photo
                    label.pack(pady=5)
                else:
                    tk.Label(frame, text="❌ Image\nNot Found", bg="#ffcccc", 
                            fg="#c00", width=18, height=10, font=("Segoe UI", 9, "bold")).pack(pady=5)
            except Exception as e:
                tk.Label(frame, text=f"⚠️ Error\n{str(e)[:20]}", bg="#fff3cd", 
                        fg="#856404", width=18, height=10, font=("Segoe UI", 8)).pack(pady=5)
            
            info_frame = tk.Frame(frame, bg="white")
            info_frame.pack(fill=tk.X, padx=5, pady=5)
            
            tk.Label(info_frame, text=f"📐 {img_data.get('layout', 'N/A').upper()}", 
                    bg="white", font=("Segoe UI", 8, "bold"), fg="#3f51b5").pack()
            tk.Label(info_frame, text=f"📏 {img_data.get('height', 0)}px", 
                    bg="white", font=("Segoe UI", 8)).pack()
            
            tk.Button(frame, text="✏️ Edit", command=lambda idx=i: self.select_image(idx),
                     bg="#2196F3", fg="white", font=("Segoe UI", 9, "bold"),
                     cursor="hand2", relief=tk.FLAT, pady=6).pack(fill=tk.X, padx=5, pady=5)
    
    def select_image(self, index):
        self.current_image_index = index
        gallery = self.data["galleries"][self.current_gallery_index]
        img_data = gallery["images"][index]
        
        self.src_entry.delete(0, tk.END)
        self.src_entry.insert(0, img_data.get("src", ""))
        
        self.alt_text.delete("1.0", tk.END)
        self.alt_text.insert("1.0", img_data.get("alt", ""))
        
        self.layout_var.set(img_data.get("layout", "wide"))
        
        self.height_entry.delete(0, tk.END)
        self.height_entry.insert(0, str(img_data.get("height", 250)))
        
        try:
            img_path = img_data.get("src", "")
            if img_path.startswith('/'):
                img_path = img_path[1:]
            
            if os.path.exists(img_path):
                img = Image.open(img_path)
                img.thumbnail((320, 320))
                photo = ImageTk.PhotoImage(img)
                self.preview_label.config(image=photo, text="")
                self.preview_label.image = photo
            else:
                self.preview_label.config(text="Preview Unavailable\n\nFile not found", image="")
                self.preview_label.image = None
        except Exception as e:
            self.preview_label.config(text=f"Preview Error\n\n{str(e)}", image="")
            self.preview_label.image = None
    
    def update_image(self):
        if self.current_gallery_index is None or self.current_image_index is None:
            messagebox.showwarning("Warning", "No image selected!")
            return
        
        gallery = self.data["galleries"][self.current_gallery_index]
        img_data = gallery["images"][self.current_image_index]
        
        img_data["src"] = self.src_entry.get()
        img_data["alt"] = self.alt_text.get("1.0", tk.END).strip()
        img_data["layout"] = self.layout_var.get()
        
        try:
            img_data["height"] = int(self.height_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Height must be a number!")
            return
        
        self.mark_unsaved()
        self.display_gallery_images()
        messagebox.showinfo("Updated ✓", "Image properties updated!")
    
    def add_image(self):
        if self.current_gallery_index is None:
            messagebox.showwarning("Warning", "Select a gallery first!")
            return
        
        gallery = self.data["galleries"][self.current_gallery_index]
        
        new_image = {
            "src": "/images/placeholder.webp",
            "alt": "New Image - Add Description Here",
            "layout": "wide",
            "height": 250
        }
        
        gallery["images"].append(new_image)
        self.mark_unsaved()
        self.display_gallery_images()
        messagebox.showinfo("Added ✓", "New image slot created!")
    
    def delete_image(self):
        if self.current_gallery_index is None or self.current_image_index is None:
            messagebox.showwarning("Warning", "No image selected!")
            return
        
        if messagebox.askyesno("Confirm Delete", "Delete this image from the gallery?"):
            gallery = self.data["galleries"][self.current_gallery_index]
            del gallery["images"][self.current_image_index]
            self.current_image_index = None
            self.mark_unsaved()
            self.display_gallery_images()
            
            self.src_entry.delete(0, tk.END)
            self.alt_text.delete("1.0", tk.END)
            self.height_entry.delete(0, tk.END)
            self.preview_label.config(image="", text="Image deleted")
            self.preview_label.image = None
    
    def move_image(self, direction):
        if self.current_image_index is None:
            messagebox.showwarning("Warning", "No image selected!")
            return
        
        gallery = self.data["galleries"][self.current_gallery_index]
        images = gallery["images"]
        new_index = self.current_image_index + direction
        
        if 0 <= new_index < len(images):
            images[self.current_image_index], images[new_index] = \
                images[new_index], images[self.current_image_index]
            self.current_image_index = new_index
            self.mark_unsaved()
            self.display_gallery_images()
        else:
            messagebox.showinfo("Info", "Can't move further in that direction!")
    
    def add_gallery(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Gallery Section")
        dialog.geometry("500x400")
        dialog.configure(bg="white")
        
        tk.Label(dialog, text="📁 Create New Gallery Section", 
                font=("Segoe UI", 14, "bold"), bg="#3f51b5", fg="white", pady=15).pack(fill=tk.X)
        
        form_frame = tk.Frame(dialog, bg="white")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(form_frame, text="Gallery Title:", font=("Segoe UI", 10, "bold"), 
                bg="white").pack(anchor='w', pady=(10,5))
        title_entry = tk.Entry(form_frame, width=50, font=("Segoe UI", 10))
        title_entry.pack(fill=tk.X)
        title_entry.focus()
        
        tk.Label(form_frame, text="Description:", font=("Segoe UI", 10, "bold"), 
                bg="white").pack(anchor='w', pady=(15,5))
        desc_text = tk.Text(form_frame, width=50, height=6, font=("Segoe UI", 10), wrap=tk.WORD)
        desc_text.pack(fill=tk.BOTH, expand=True)
        
        def save_gallery():
            title = title_entry.get().strip()
            if not title:
                messagebox.showwarning("Warning", "Please enter a title!")
                return
            
            new_gallery = {
                "id": title.lower().replace(" ", "-").replace("&", "and"),
                "title": title,
                "description": desc_text.get("1.0", tk.END).strip(),
                "images": []
            }
            self.data["galleries"].append(new_gallery)
            self.mark_unsaved()
            self.refresh_gallery_list()
            dialog.destroy()
            messagebox.showinfo("Success ✓", f"Gallery '{title}' created!")
        
        tk.Button(form_frame, text="✅ Create Gallery", command=save_gallery,
                 bg="#4CAF50", fg="white", font=("Segoe UI", 11, "bold"),
                 cursor="hand2", relief=tk.FLAT, pady=10).pack(fill=tk.X, pady=20)
    
    def edit_gallery(self):
        if self.current_gallery_index is None:
            messagebox.showwarning("Warning", "Select a gallery first!")
            return
        
        gallery = self.data["galleries"][self.current_gallery_index]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Gallery Section")
        dialog.geometry("500x400")
        dialog.configure(bg="white")
        
        tk.Label(dialog, text="✏️ Edit Gallery Section", 
                font=("Segoe UI", 14, "bold"), bg="#2196F3", fg="white", pady=15).pack(fill=tk.X)
        
        form_frame = tk.Frame(dialog, bg="white")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(form_frame, text="Gallery Title:", font=("Segoe UI", 10, "bold"), 
                bg="white").pack(anchor='w', pady=(10,5))
        title_entry = tk.Entry(form_frame, width=50, font=("Segoe UI", 10))
        title_entry.insert(0, gallery.get("title", ""))
        title_entry.pack(fill=tk.X)
        
        tk.Label(form_frame, text="Description:", font=("Segoe UI", 10, "bold"), 
                bg="white").pack(anchor='w', pady=(15,5))
        desc_text = tk.Text(form_frame, width=50, height=6, font=("Segoe UI", 10), wrap=tk.WORD)
        desc_text.insert("1.0", gallery.get("description", ""))
        desc_text.pack(fill=tk.BOTH, expand=True)
        
        def save_changes():
            gallery["title"] = title_entry.get()
            gallery["description"] = desc_text.get("1.0", tk.END).strip()
            gallery["id"] = gallery["title"].lower().replace(" ", "-").replace("&", "and")
            self.mark_unsaved()
            self.refresh_gallery_list()
            dialog.destroy()
            messagebox.showinfo("Saved ✓", "Gallery updated!")
        
        tk.Button(form_frame, text="💾 Save Changes", command=save_changes,
                 bg="#2196F3", fg="white", font=("Segoe UI", 11, "bold"),
                 cursor="hand2", relief=tk.FLAT, pady=10).pack(fill=tk.X, pady=20)
    
    def delete_gallery(self):
        if self.current_gallery_index is None:
            messagebox.showwarning("Warning", "Select a gallery first!")
            return
        
        gallery = self.data["galleries"][self.current_gallery_index]
        title = gallery.get("title", "this gallery")
        
        if messagebox.askyesno("Confirm Delete", 
                              f"Delete '{title}' and all {len(gallery.get('images', []))} images?\n\nThis cannot be undone!"):
            del self.data["galleries"][self.current_gallery_index]
            self.current_gallery_index = None
            self.current_image_index = None
            self.mark_unsaved()
            self.refresh_gallery_list()
            
            for widget in self.images_frame.winfo_children():
                widget.destroy()
            self.gallery_info.config(text="Select a gallery section from the left")
    
    def browse_image(self):
        filename = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.webp *.gif"),
                ("All files", "*.*")
            ]
        )
        if filename:
            try:
                rel_path = os.path.relpath(filename)
                if not rel_path.startswith('/'):
                    rel_path = '/' + rel_path.replace('\\', '/')
                self.src_entry.delete(0, tk.END)
                self.src_entry.insert(0, rel_path)
                self.mark_unsaved()
            except:
                self.src_entry.delete(0, tk.END)
                self.src_entry.insert(0, filename)
                self.mark_unsaved()
    
    def apply_preset(self, layout, height):
        self.layout_var.set(layout)
        self.height_entry.delete(0, tk.END)
        self.height_entry.insert(0, str(height))
        self.mark_unsaved()
        messagebox.showinfo("Preset Applied ✓", f"Layout: {layout.upper()}\nHeight: {height}px\n\nClick 'Update Image' to save.")
    
    def show_guide(self):
        guide_text = """
Quick Start Guide:

1. CREATE/OPEN FILE
   • File > Open gallery.json (or auto-loaded if exists)
   • File > Save As to create new gallery.json

2. ADD GALLERY SECTION
   • Click "➕ Add Gallery" in left panel
   • Enter title and description
   • Click "Create Gallery"

3. ADD IMAGES
   • Select a gallery section
   • Click "➕ Add Image" at bottom
   • Click "✏️ Edit" on the image card

4. EDIT IMAGE PROPERTIES
   • Browse for image file (📁 button)
   • Write SEO-friendly alt text
   • Choose layout type (tall, wide, square, etc.)
   • Set height in pixels
   • Click "💾 Update Image"

5. AUTO-SAVE
   • Enabled by default (every 10 seconds)
   • Toggle in File menu
   • Manual save: Ctrl+S or File > Save

6. TEST IN BROWSER
   • Server > Start Local Server
   • Server > Open in Browser
   • View gallery.html to see your changes

7. REORDER IMAGES
   • Select image with "✏️ Edit"
   • Use "⬆️ Move Up" or "⬇️ Move Down"

TIP: Keep gallery.html in same folder as gallery.json!
        """
        messagebox.showinfo("Quick Start Guide", guide_text)
    
    def show_about(self):
        about_text = """
🎨 Tech Engineer Gallery JSON Editor
Version 2.0 - Enhanced Edition

Features:
✓ Auto-load gallery.json on startup
✓ Auto-save every 10 seconds
✓ Built-in local server for testing
✓ Visual image preview
✓ SEO-friendly alt text editing
✓ Quick layout presets
✓ Drag-and-drop image reordering
✓ Unsaved changes indicator (*)

Local Server:
• Serves gallery.json via HTTP
• Test gallery.html in browser
• No CORS errors!

Keyboard Shortcuts:
Ctrl+O - Open file
Ctrl+S - Save file

Developed for Tech Engineer
Mohali, Punjab

© 2025 All Rights Reserved
        """
        messagebox.showinfo("About Gallery Editor", about_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = GalleryJSONEditor(root)
    root.mainloop()