import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import json
import os
import shutil
from datetime import datetime


class BlogManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📝 Blog Post Manager")
        self.root.geometry("1400x850")
        self.root.configure(bg="#1a1a2e")
        self.root.minsize(1200, 700)

        # --- Data ---
        self.blog_data = []
        self.selected_index = None
        self.image_path_var = tk.StringVar()
        self.json_file_path = None

        # --- Category/Badge Presets ---
        self.category_presets = {
            "AI & Tech": {"badgeClass": "bg-primary-gradient", "badgeIcon": "fas fa-robot"},
            "Podcast": {"badgeClass": "bg-warning-gradient", "badgeIcon": "fas fa-microphone-alt"},
            "E-Commerce": {"badgeClass": "bg-purple-gradient", "badgeIcon": "fas fa-shopping-cart"},
            "Tutorial": {"badgeClass": "bg-success-gradient", "badgeIcon": "fas fa-book"},
            "News": {"badgeClass": "bg-danger-gradient", "badgeIcon": "fas fa-newspaper"},
            "Review": {"badgeClass": "bg-info-gradient", "badgeIcon": "fas fa-star"},
            "Custom": {"badgeClass": "", "badgeIcon": ""},
        }

        # --- Styles ---
        self.setup_styles()

        # --- Build UI ---
        self.build_menu()
        self.build_toolbar()
        self.build_main_layout()

        # --- Load sample data ---
        self.load_sample_data()

    # =========================================================================
    # STYLES
    # =========================================================================
    def setup_styles(self):
        self.colors = {
            "bg_dark": "#1a1a2e",
            "bg_card": "#16213e",
            "bg_input": "#0f3460",
            "bg_hover": "#1f4287",
            "accent": "#e94560",
            "accent2": "#533483",
            "text": "#eee",
            "text_dim": "#a0a0b0",
            "success": "#00b894",
            "warning": "#fdcb6e",
            "danger": "#d63031",
            "border": "#2c3e6b",
        }

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Dark.TFrame", background=self.colors["bg_dark"])
        style.configure("Card.TFrame", background=self.colors["bg_card"])
        style.configure(
            "Dark.TLabel",
            background=self.colors["bg_card"],
            foreground=self.colors["text"],
            font=("Segoe UI", 10),
        )
        style.configure(
            "Title.TLabel",
            background=self.colors["bg_dark"],
            foreground=self.colors["text"],
            font=("Segoe UI", 18, "bold"),
        )
        style.configure(
            "Heading.TLabel",
            background=self.colors["bg_card"],
            foreground=self.colors["accent"],
            font=("Segoe UI", 12, "bold"),
        )
        style.configure(
            "Accent.TButton",
            background=self.colors["accent"],
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            padding=(15, 8),
        )
        style.map(
            "Accent.TButton",
            background=[("active", "#c0392b")],
        )
        style.configure(
            "Success.TButton",
            background=self.colors["success"],
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            padding=(15, 8),
        )
        style.map("Success.TButton", background=[("active", "#00a884")])
        style.configure(
            "Warning.TButton",
            background=self.colors["warning"],
            foreground="#222",
            font=("Segoe UI", 10, "bold"),
            padding=(15, 8),
        )
        style.configure(
            "Danger.TButton",
            background=self.colors["danger"],
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            padding=(15, 8),
        )
        style.map("Danger.TButton", background=[("active", "#b71c1c")])
        style.configure(
            "Toolbar.TButton",
            background=self.colors["bg_input"],
            foreground=self.colors["text"],
            font=("Segoe UI", 9),
            padding=(10, 5),
        )
        style.map(
            "Toolbar.TButton",
            background=[("active", self.colors["bg_hover"])],
        )

        style.configure(
            "Treeview",
            background=self.colors["bg_card"],
            foreground=self.colors["text"],
            fieldbackground=self.colors["bg_card"],
            borderwidth=0,
            font=("Segoe UI", 10),
            rowheight=40,
        )
        style.configure(
            "Treeview.Heading",
            background=self.colors["bg_input"],
            foreground=self.colors["text"],
            font=("Segoe UI", 10, "bold"),
            borderwidth=0,
        )
        style.map(
            "Treeview",
            background=[("selected", self.colors["accent"])],
            foreground=[("selected", "white")],
        )

    # =========================================================================
    # MENU BAR
    # =========================================================================
    def build_menu(self):
        menubar = tk.Menu(self.root, bg=self.colors["bg_dark"], fg=self.colors["text"],
                          activebackground=self.colors["accent"], activeforeground="white",
                          font=("Segoe UI", 10))

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0, bg=self.colors["bg_card"],
                            fg=self.colors["text"], activebackground=self.colors["accent"],
                            font=("Segoe UI", 10))
        file_menu.add_command(label="📂 Open JSON File", command=self.open_json_file, accelerator="Ctrl+O")
        file_menu.add_command(label="💾 Save JSON File", command=self.save_json_file, accelerator="Ctrl+S")
        file_menu.add_command(label="💾 Save As...", command=self.save_json_as)
        file_menu.add_separator()
        file_menu.add_command(label="📋 Load Sample Data", command=self.load_sample_data)
        file_menu.add_separator()
        file_menu.add_command(label="🚪 Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0, bg=self.colors["bg_card"],
                            fg=self.colors["text"], activebackground=self.colors["accent"],
                            font=("Segoe UI", 10))
        edit_menu.add_command(label="➕ New Entry", command=self.clear_form, accelerator="Ctrl+N")
        edit_menu.add_command(label="🗑️ Delete Selected", command=self.delete_entry, accelerator="Delete")
        edit_menu.add_command(label="📋 Duplicate Selected", command=self.duplicate_entry)
        edit_menu.add_separator()
        edit_menu.add_command(label="⬆️ Move Up", command=self.move_up)
        edit_menu.add_command(label="⬇️ Move Down", command=self.move_down)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0, bg=self.colors["bg_card"],
                            fg=self.colors["text"], activebackground=self.colors["accent"],
                            font=("Segoe UI", 10))
        help_menu.add_command(label="ℹ️ About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

        # Keyboard shortcuts
        self.root.bind("<Control-o>", lambda e: self.open_json_file())
        self.root.bind("<Control-s>", lambda e: self.save_json_file())
        self.root.bind("<Control-n>", lambda e: self.clear_form())
        self.root.bind("<Delete>", lambda e: self.delete_entry())

    # =========================================================================
    # TOOLBAR
    # =========================================================================
    def build_toolbar(self):
        toolbar = tk.Frame(self.root, bg=self.colors["bg_input"], height=45)
        toolbar.pack(fill="x", side="top")
        toolbar.pack_propagate(False)

        buttons = [
            ("📂 Open", self.open_json_file),
            ("💾 Save", self.save_json_file),
            ("➕ New", self.clear_form),
            ("📋 Duplicate", self.duplicate_entry),
            ("🗑️ Delete", self.delete_entry),
            ("⬆️ Up", self.move_up),
            ("⬇️ Down", self.move_down),
        ]

        for text, cmd in buttons:
            btn = tk.Button(
                toolbar, text=text, command=cmd,
                bg=self.colors["bg_input"], fg=self.colors["text"],
                activebackground=self.colors["bg_hover"], activeforeground="white",
                font=("Segoe UI", 9), bd=0, padx=12, pady=5,
                cursor="hand2", relief="flat",
            )
            btn.pack(side="left", padx=2, pady=5)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.colors["bg_hover"]))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.colors["bg_input"]))

        # Entry count label
        self.count_label = tk.Label(
            toolbar, text="Entries: 0", bg=self.colors["bg_input"],
            fg=self.colors["warning"], font=("Segoe UI", 10, "bold"),
        )
        self.count_label.pack(side="right", padx=15)

        # Search
        tk.Label(toolbar, text="🔍", bg=self.colors["bg_input"],
                 fg=self.colors["text"], font=("Segoe UI", 12)).pack(side="right")
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.filter_list)
        search_entry = tk.Entry(
            toolbar, textvariable=self.search_var,
            bg=self.colors["bg_dark"], fg=self.colors["text"],
            insertbackground=self.colors["text"], font=("Segoe UI", 10),
            bd=0, width=20,
        )
        search_entry.pack(side="right", padx=5, pady=8)

    # =========================================================================
    # MAIN LAYOUT
    # =========================================================================
    def build_main_layout(self):
        # Main container
        main_pane = tk.PanedWindow(
            self.root, orient="horizontal",
            bg=self.colors["bg_dark"], sashwidth=4,
            sashrelief="flat",
        )
        main_pane.pack(fill="both", expand=True, padx=5, pady=5)

        # LEFT PANEL - List
        left_frame = tk.Frame(main_pane, bg=self.colors["bg_dark"])
        main_pane.add(left_frame, width=550)

        tk.Label(
            left_frame, text="📋 Blog Entries",
            bg=self.colors["bg_dark"], fg=self.colors["text"],
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w", padx=10, pady=(10, 5))

        # Treeview
        tree_frame = tk.Frame(left_frame, bg=self.colors["border"])
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("title", "category", "date")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("title", text="Title", anchor="w")
        self.tree.heading("category", text="Category", anchor="w")
        self.tree.heading("date", text="Date", anchor="w")
        self.tree.column("title", width=250, minwidth=150)
        self.tree.column("category", width=100, minwidth=80)
        self.tree.column("date", width=120, minwidth=100)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        self.tree.tag_configure("even", background=self.colors["bg_card"])
        self.tree.tag_configure("odd", background="#1b2a4a")

        # RIGHT PANEL - Form
        right_frame = tk.Frame(main_pane, bg=self.colors["bg_dark"])
        main_pane.add(right_frame, width=820)

        # Scrollable form
        canvas = tk.Canvas(right_frame, bg=self.colors["bg_dark"], highlightthickness=0)
        form_scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)
        self.form_container = tk.Frame(canvas, bg=self.colors["bg_dark"])

        self.form_container.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.form_container, anchor="nw")
        canvas.configure(yscrollcommand=form_scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        form_scrollbar.pack(side="right", fill="y")

        # Mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        self.build_form()

    # =========================================================================
    # FORM
    # =========================================================================
    def build_form(self):
        parent = self.form_container

        # Title bar
        title_bar = tk.Frame(parent, bg=self.colors["accent"], height=50)
        title_bar.pack(fill="x", padx=10, pady=(10, 0))
        title_bar.pack_propagate(False)
        self.form_title_label = tk.Label(
            title_bar, text="➕ New Blog Entry",
            bg=self.colors["accent"], fg="white",
            font=("Segoe UI", 14, "bold"),
        )
        self.form_title_label.pack(side="left", padx=15, pady=10)

        # Form card
        form_card = tk.Frame(parent, bg=self.colors["bg_card"], bd=0)
        form_card.pack(fill="x", padx=10, pady=(0, 10))

        inner = tk.Frame(form_card, bg=self.colors["bg_card"])
        inner.pack(fill="x", padx=20, pady=15)

        self.entries = {}
        row = 0

        # --- TITLE ---
        row = self._add_field(inner, row, "title", "📌 Title", "Enter blog post title...")

        # --- IMAGE ---
        tk.Label(inner, text="🖼️ Image Path", bg=self.colors["bg_card"],
                 fg=self.colors["accent"], font=("Segoe UI", 10, "bold")).grid(
            row=row, column=0, sticky="w", pady=(10, 2), columnspan=2
        )
        row += 1

        img_frame = tk.Frame(inner, bg=self.colors["bg_card"])
        img_frame.grid(row=row, column=0, sticky="ew", columnspan=2, pady=(0, 5))
        img_frame.columnconfigure(0, weight=1)

        self.entries["image"] = tk.Entry(
            img_frame, bg=self.colors["bg_input"], fg=self.colors["text"],
            insertbackground=self.colors["text"], font=("Segoe UI", 10),
            bd=0, relief="flat",
        )
        self.entries["image"].pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 5))

        tk.Button(
            img_frame, text="📁 Browse", command=self.browse_image,
            bg=self.colors["accent2"], fg="white", font=("Segoe UI", 9, "bold"),
            bd=0, padx=12, pady=4, cursor="hand2",
        ).pack(side="right")
        row += 1

        # Image preview
        self.image_preview_frame = tk.Frame(inner, bg=self.colors["bg_card"], width=200, height=130)
        self.image_preview_frame.grid(row=row, column=0, sticky="w", columnspan=2, pady=5)
        self.image_preview_frame.pack_propagate(False)

        self.image_preview_label = tk.Label(
            self.image_preview_frame, text="No Image Selected",
            bg=self.colors["bg_input"], fg=self.colors["text_dim"],
            font=("Segoe UI", 9),
        )
        self.image_preview_label.pack(fill="both", expand=True)
        row += 1

        # --- CATEGORY (Dropdown) ---
        tk.Label(inner, text="🏷️ Category", bg=self.colors["bg_card"],
                 fg=self.colors["accent"], font=("Segoe UI", 10, "bold")).grid(
            row=row, column=0, sticky="w", pady=(10, 2), columnspan=2
        )
        row += 1

        cat_frame = tk.Frame(inner, bg=self.colors["bg_card"])
        cat_frame.grid(row=row, column=0, sticky="ew", columnspan=2, pady=(0, 5))
        cat_frame.columnconfigure(0, weight=1)

        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(
            cat_frame, textvariable=self.category_var,
            values=list(self.category_presets.keys()),
            font=("Segoe UI", 10), state="normal",
        )
        self.category_combo.pack(side="left", fill="x", expand=True, ipady=4)
        self.category_combo.bind("<<ComboboxSelected>>", self.on_category_change)
        row += 1

        # --- BADGE CLASS ---
        row = self._add_field(inner, row, "badgeClass", "🎨 Badge Class", "e.g. bg-primary-gradient")

        # --- BADGE ICON ---
        row = self._add_field(inner, row, "badgeIcon", "🔷 Badge Icon", "e.g. fas fa-robot")

        # --- DATE ---
        tk.Label(inner, text="📅 Date", bg=self.colors["bg_card"],
                 fg=self.colors["accent"], font=("Segoe UI", 10, "bold")).grid(
            row=row, column=0, sticky="w", pady=(10, 2), columnspan=2
        )
        row += 1

        date_frame = tk.Frame(inner, bg=self.colors["bg_card"])
        date_frame.grid(row=row, column=0, sticky="ew", columnspan=2, pady=(0, 5))
        date_frame.columnconfigure(0, weight=1)

        self.entries["date"] = tk.Entry(
            date_frame, bg=self.colors["bg_input"], fg=self.colors["text"],
            insertbackground=self.colors["text"], font=("Segoe UI", 10),
            bd=0, relief="flat",
        )
        self.entries["date"].pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 5))

        tk.Button(
            date_frame, text="📅 Today", command=self.set_today_date,
            bg=self.colors["success"], fg="white", font=("Segoe UI", 9, "bold"),
            bd=0, padx=10, pady=4, cursor="hand2",
        ).pack(side="right")
        row += 1

        # --- AUTHOR ---
        row = self._add_field(inner, row, "author", "✍️ Author", "Author name...")

        # --- EXCERPT ---
        tk.Label(inner, text="📝 Excerpt", bg=self.colors["bg_card"],
                 fg=self.colors["accent"], font=("Segoe UI", 10, "bold")).grid(
            row=row, column=0, sticky="w", pady=(10, 2), columnspan=2
        )
        row += 1

        self.excerpt_text = tk.Text(
            inner, bg=self.colors["bg_input"], fg=self.colors["text"],
            insertbackground=self.colors["text"], font=("Segoe UI", 10),
            bd=0, relief="flat", height=4, wrap="word",
        )
        self.excerpt_text.grid(row=row, column=0, sticky="ew", columnspan=2, pady=(0, 5), ipady=4)
        row += 1

        # --- LINK ---
        row = self._add_field(inner, row, "link", "🔗 Link / URL", "https://...")

        # --- TARGET ---
        tk.Label(inner, text="🎯 Target", bg=self.colors["bg_card"],
                 fg=self.colors["accent"], font=("Segoe UI", 10, "bold")).grid(
            row=row, column=0, sticky="w", pady=(10, 2), columnspan=2
        )
        row += 1

        self.target_var = tk.StringVar(value="_self")
        target_frame = tk.Frame(inner, bg=self.colors["bg_card"])
        target_frame.grid(row=row, column=0, sticky="w", columnspan=2, pady=(0, 5))

        for val, label in [("_self", "Same Tab (_self)"), ("_blank", "New Tab (_blank)")]:
            tk.Radiobutton(
                target_frame, text=label, variable=self.target_var, value=val,
                bg=self.colors["bg_card"], fg=self.colors["text"],
                selectcolor=self.colors["bg_input"], activebackground=self.colors["bg_card"],
                activeforeground=self.colors["text"], font=("Segoe UI", 10),
                cursor="hand2",
            ).pack(side="left", padx=(0, 20))
        row += 1

        # --- BUTTON TEXT ---
        row = self._add_field(inner, row, "btnText", "🔘 Button Text", "e.g. Read Article")

        # --- BUTTON ICON ---
        row = self._add_field(inner, row, "btnIcon", "✨ Button Icon", "e.g. fas fa-arrow-right")

        inner.columnconfigure(0, weight=1)

        # --- ACTION BUTTONS ---
        btn_frame = tk.Frame(parent, bg=self.colors["bg_dark"])
        btn_frame.pack(fill="x", padx=10, pady=(0, 15))

        self.save_btn = tk.Button(
            btn_frame, text="💾 Save Entry", command=self.save_entry,
            bg=self.colors["success"], fg="white", font=("Segoe UI", 11, "bold"),
            bd=0, padx=25, pady=10, cursor="hand2", activebackground="#00a884",
        )
        self.save_btn.pack(side="left", padx=(0, 10))

        self.update_btn = tk.Button(
            btn_frame, text="✏️ Update Entry", command=self.update_entry,
            bg=self.colors["warning"], fg="#222", font=("Segoe UI", 11, "bold"),
            bd=0, padx=25, pady=10, cursor="hand2", state="disabled",
        )
        self.update_btn.pack(side="left", padx=(0, 10))

        tk.Button(
            btn_frame, text="🧹 Clear Form", command=self.clear_form,
            bg=self.colors["bg_input"], fg=self.colors["text"],
            font=("Segoe UI", 11, "bold"), bd=0, padx=25, pady=10,
            cursor="hand2", activebackground=self.colors["bg_hover"],
        ).pack(side="left", padx=(0, 10))

        tk.Button(
            btn_frame, text="🗑️ Delete", command=self.delete_entry,
            bg=self.colors["danger"], fg="white", font=("Segoe UI", 11, "bold"),
            bd=0, padx=25, pady=10, cursor="hand2", activebackground="#b71c1c",
        ).pack(side="right")

        # Status bar
        self.status_bar = tk.Label(
            parent, text="Ready", bg=self.colors["bg_input"],
            fg=self.colors["text_dim"], font=("Segoe UI", 9),
            anchor="w", padx=15, pady=5,
        )
        self.status_bar.pack(fill="x", padx=10, pady=(0, 10))

    def _add_field(self, parent, row, key, label, placeholder=""):
        tk.Label(parent, text=label, bg=self.colors["bg_card"],
                 fg=self.colors["accent"], font=("Segoe UI", 10, "bold")).grid(
            row=row, column=0, sticky="w", pady=(10, 2), columnspan=2
        )
        row += 1

        entry = tk.Entry(
            parent, bg=self.colors["bg_input"], fg=self.colors["text"],
            insertbackground=self.colors["text"], font=("Segoe UI", 10),
            bd=0, relief="flat",
        )
        entry.grid(row=row, column=0, sticky="ew", columnspan=2, ipady=6, pady=(0, 5))
        entry.insert(0, "")
        self.entries[key] = entry

        # Placeholder behavior
        if placeholder:
            entry.insert(0, placeholder)
            entry.config(fg=self.colors["text_dim"])
            entry.bind("<FocusIn>", lambda e, en=entry, ph=placeholder: self._clear_placeholder(en, ph))
            entry.bind("<FocusOut>", lambda e, en=entry, ph=placeholder: self._set_placeholder(en, ph))

        row += 1
        return row

    def _clear_placeholder(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, "end")
            entry.config(fg=self.colors["text"])

    def _set_placeholder(self, entry, placeholder):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg=self.colors["text_dim"])

    # =========================================================================
    # ACTIONS
    # =========================================================================
    def browse_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.webp *.gif *.bmp"),
                ("All Files", "*.*"),
            ],
        )
        if file_path:
            self.entries["image"].delete(0, "end")
            self.entries["image"].config(fg=self.colors["text"])
            self.entries["image"].insert(0, file_path)
            self.show_image_preview(file_path)
            self.set_status(f"Image selected: {os.path.basename(file_path)}")

    def show_image_preview(self, path):
        try:
            if os.path.exists(path):
                img = Image.open(path)
                img.thumbnail((200, 120))
                photo = ImageTk.PhotoImage(img)
                self.image_preview_label.config(image=photo, text="")
                self.image_preview_label.image = photo
            else:
                self.image_preview_label.config(image="", text=f"📁 {path}")
        except Exception:
            self.image_preview_label.config(image="", text=f"📁 {path}")

    def on_category_change(self, event=None):
        category = self.category_var.get()
        if category in self.category_presets:
            preset = self.category_presets[category]
            if preset["badgeClass"]:
                self.entries["badgeClass"].delete(0, "end")
                self.entries["badgeClass"].config(fg=self.colors["text"])
                self.entries["badgeClass"].insert(0, preset["badgeClass"])
            if preset["badgeIcon"]:
                self.entries["badgeIcon"].delete(0, "end")
                self.entries["badgeIcon"].config(fg=self.colors["text"])
                self.entries["badgeIcon"].insert(0, preset["badgeIcon"])

    def set_today_date(self):
        today = datetime.now().strftime("%B %d, %Y")
        self.entries["date"].delete(0, "end")
        self.entries["date"].config(fg=self.colors["text"])
        self.entries["date"].insert(0, today)

    def get_field_value(self, key):
        """Get field value, ignoring placeholder text."""
        if key == "excerpt":
            return self.excerpt_text.get("1.0", "end-1c").strip()
        if key == "category":
            return self.category_var.get().strip()
        if key == "target":
            return self.target_var.get()

        entry = self.entries.get(key)
        if not entry:
            return ""
        val = entry.get().strip()
        # Check for placeholder values
        placeholders = [
            "Enter blog post title...", "e.g. bg-primary-gradient",
            "e.g. fas fa-robot", "Author name...", "https://...",
            "e.g. Read Article", "e.g. fas fa-arrow-right",
        ]
        if val in placeholders:
            return ""
        return val

    def set_field_value(self, key, value):
        if key == "excerpt":
            self.excerpt_text.delete("1.0", "end")
            self.excerpt_text.insert("1.0", value or "")
            return
        if key == "category":
            self.category_var.set(value or "")
            return
        if key == "target":
            self.target_var.set(value or "_self")
            return

        entry = self.entries.get(key)
        if entry:
            entry.delete(0, "end")
            entry.config(fg=self.colors["text"])
            entry.insert(0, value or "")

    def collect_form_data(self):
        data = {}
        fields = ["title", "image", "badgeClass", "badgeIcon", "date",
                  "author", "link", "btnText", "btnIcon"]
        for f in fields:
            data[f] = self.get_field_value(f)
        data["category"] = self.get_field_value("category")
        data["excerpt"] = self.get_field_value("excerpt")
        data["target"] = self.get_field_value("target")
        return data

    def validate_form(self, data):
        if not data.get("title"):
            messagebox.showwarning("⚠️ Validation", "Title is required!")
            return False
        return True

    def save_entry(self):
        data = self.collect_form_data()
        if not self.validate_form(data):
            return

        self.blog_data.append(data)
        self.refresh_tree()
        self.clear_form()
        self.set_status(f"✅ Entry added: {data['title']}")

    def update_entry(self):
        if self.selected_index is None:
            messagebox.showinfo("Info", "No entry selected to update.")
            return

        data = self.collect_form_data()
        if not self.validate_form(data):
            return

        self.blog_data[self.selected_index] = data
        self.refresh_tree()
        self.set_status(f"✏️ Entry updated: {data['title']}")

        # Re-select the item
        children = self.tree.get_children()
        if self.selected_index < len(children):
            self.tree.selection_set(children[self.selected_index])

    def delete_entry(self):
        if self.selected_index is None:
            messagebox.showinfo("Info", "No entry selected to delete.")
            return

        title = self.blog_data[self.selected_index].get("title", "Untitled")
        if messagebox.askyesno("🗑️ Confirm Delete", f'Delete "{title}"?'):
            del self.blog_data[self.selected_index]
            self.selected_index = None
            self.refresh_tree()
            self.clear_form()
            self.set_status(f"🗑️ Deleted: {title}")

    def duplicate_entry(self):
        if self.selected_index is None:
            messagebox.showinfo("Info", "No entry selected to duplicate.")
            return

        import copy
        dup = copy.deepcopy(self.blog_data[self.selected_index])
        dup["title"] = dup.get("title", "") + " (Copy)"
        self.blog_data.insert(self.selected_index + 1, dup)
        self.refresh_tree()
        self.set_status(f"📋 Duplicated: {dup['title']}")

    def move_up(self):
        if self.selected_index is None or self.selected_index <= 0:
            return
        i = self.selected_index
        self.blog_data[i], self.blog_data[i - 1] = self.blog_data[i - 1], self.blog_data[i]
        self.selected_index -= 1
        self.refresh_tree()
        self.tree.selection_set(self.tree.get_children()[self.selected_index])
        self.set_status("⬆️ Moved up")

    def move_down(self):
        if self.selected_index is None or self.selected_index >= len(self.blog_data) - 1:
            return
        i = self.selected_index
        self.blog_data[i], self.blog_data[i + 1] = self.blog_data[i + 1], self.blog_data[i]
        self.selected_index += 1
        self.refresh_tree()
        self.tree.selection_set(self.tree.get_children()[self.selected_index])
        self.set_status("⬇️ Moved down")

    def clear_form(self):
        for key, entry in self.entries.items():
            entry.delete(0, "end")
            entry.config(fg=self.colors["text"])

        self.excerpt_text.delete("1.0", "end")
        self.category_var.set("")
        self.target_var.set("_self")
        self.image_preview_label.config(image="", text="No Image Selected")
        self.image_preview_label.image = None

        self.selected_index = None
        self.form_title_label.config(text="➕ New Blog Entry")
        self.update_btn.config(state="disabled")
        self.save_btn.config(state="normal")
        self.tree.selection_remove(*self.tree.selection())
        self.set_status("Form cleared — ready for new entry")

    def on_select(self, event):
        selection = self.tree.selection()
        if not selection:
            return

        item = selection[0]
        idx = self.tree.index(item)

        # Handle search filtering
        if hasattr(self, "_filtered_indices"):
            idx = self._filtered_indices[idx]

        self.selected_index = idx
        data = self.blog_data[idx]

        # Fill form
        fields = ["title", "image", "badgeClass", "badgeIcon", "date",
                  "author", "link", "btnText", "btnIcon"]
        for f in fields:
            self.set_field_value(f, data.get(f, ""))

        self.set_field_value("category", data.get("category", ""))
        self.set_field_value("excerpt", data.get("excerpt", ""))
        self.set_field_value("target", data.get("target", "_self"))

        # Image preview
        img_path = data.get("image", "")
        if img_path:
            self.show_image_preview(img_path)
        else:
            self.image_preview_label.config(image="", text="No Image Selected")

        self.form_title_label.config(text=f"✏️ Edit: {data.get('title', 'Untitled')}")
        self.update_btn.config(state="normal")
        self.save_btn.config(state="disabled")
        self.set_status(f"Editing: {data.get('title', 'Untitled')}")

    def refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        if hasattr(self, "_filtered_indices"):
            del self._filtered_indices

        for i, item in enumerate(self.blog_data):
            tag = "even" if i % 2 == 0 else "odd"
            self.tree.insert(
                "", "end",
                values=(
                    item.get("title", "Untitled"),
                    item.get("category", "—"),
                    item.get("date", "—"),
                ),
                tags=(tag,),
            )

        self.count_label.config(text=f"Entries: {len(self.blog_data)}")

    def filter_list(self, *args):
        query = self.search_var.get().lower().strip()
        self.tree.delete(*self.tree.get_children())

        if not query:
            if hasattr(self, "_filtered_indices"):
                del self._filtered_indices
            self.refresh_tree()
            return

        self._filtered_indices = []
        count = 0
        for i, item in enumerate(self.blog_data):
            searchable = f"{item.get('title', '')} {item.get('category', '')} {item.get('author', '')}".lower()
            if query in searchable:
                tag = "even" if count % 2 == 0 else "odd"
                self.tree.insert(
                    "", "end",
                    values=(
                        item.get("title", "Untitled"),
                        item.get("category", "—"),
                        item.get("date", "—"),
                    ),
                    tags=(tag,),
                )
                self._filtered_indices.append(i)
                count += 1

        self.count_label.config(text=f"Showing: {count}/{len(self.blog_data)}")

    # =========================================================================
    # FILE OPERATIONS
    # =========================================================================
    def open_json_file(self):
        file_path = filedialog.askopenfilename(
            title="Open JSON File",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
        )
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, list):
                self.blog_data = data
            elif isinstance(data, dict):
                self.blog_data = [data]
            else:
                messagebox.showerror("Error", "Invalid JSON structure.")
                return

            self.json_file_path = file_path
            self.refresh_tree()
            self.clear_form()
            self.set_status(f"📂 Loaded: {file_path} ({len(self.blog_data)} entries)")
            self.root.title(f"📝 Blog Manager — {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{e}")

    def save_json_file(self):
        if not self.json_file_path:
            self.save_json_as()
            return

        try:
            with open(self.json_file_path, "w", encoding="utf-8") as f:
                json.dump(self.blog_data, f, indent=4, ensure_ascii=False)
            self.set_status(f"💾 Saved: {self.json_file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save:\n{e}")

    def save_json_as(self):
        file_path = filedialog.asksaveasfilename(
            title="Save JSON File",
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
        )
        if not file_path:
            return

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self.blog_data, f, indent=4, ensure_ascii=False)
            self.json_file_path = file_path
            self.root.title(f"📝 Blog Manager — {os.path.basename(file_path)}")
            self.set_status(f"💾 Saved as: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save:\n{e}")

    # =========================================================================
    # SAMPLE DATA
    # =========================================================================
    def load_sample_data(self):
        self.blog_data = [
            {
                "title": "AI in 2026: What's Changed and What's Coming Next",
                "image": "./images/blog/ai-2026-featured1.webp",
                "category": "AI & Tech",
                "badgeClass": "bg-primary-gradient",
                "badgeIcon": "fas fa-robot",
                "date": "March 15, 2026",
                "author": "Tech Engineer Team",
                "excerpt": "Explore the future of artificial intelligence, new breakthroughs, and how AI is transforming industries, automation, and daily workflows in 2026.",
                "link": "/blogs/ai-in-2026-whats-changed-and-whats-coming-next",
                "target": "_self",
                "btnText": "Read Article",
                "btnIcon": "fas fa-arrow-right",
            },
            {
                "title": "Mr. Bhatia: From IT Groundwork to Sales Leadership",
                "image": "./images/techcast-ep3-mr-bhatia-rise.jpg",
                "category": "Podcast",
                "badgeClass": "bg-warning-gradient",
                "badgeIcon": "fas fa-microphone-alt",
                "date": "April 13, 2025",
                "author": "Puadh Punjabi Podcast",
                "excerpt": "Mr. Bhatia opens up about his journey — from tackling language barriers in South India to managing massive IT and telecom projects.",
                "link": "https://puadhpunjabipodcast.com/episode/ep3-mr-bhatia",
                "target": "_blank",
                "btnText": "Listen to Episode",
                "btnIcon": "fas fa-headphones",
            },
            {
                "title": "Akash's Digital Sales & E-Commerce Blueprint",
                "image": "./images/techcast-ep18-akash-ecommerce-smart-farming.jpg",
                "category": "E-Commerce",
                "badgeClass": "bg-purple-gradient",
                "badgeIcon": "fas fa-shopping-cart",
                "date": "July 27, 2025",
                "author": "TechCast Episode 18",
                "excerpt": "From village fields to national e-commerce platforms! Akash shares exactly how he built profitable product-based businesses.",
                "link": "https://puadhpunjabipodcast.com/episode/ep18-akash-ecommerce",
                "target": "_blank",
                "btnText": "Learn the Blueprint",
                "btnIcon": "fas fa-arrow-right",
            },
        ]
        self.refresh_tree()
        self.clear_form()
        self.set_status("📋 Sample data loaded (3 entries)")

    # =========================================================================
    # HELPERS
    # =========================================================================
    def set_status(self, message):
        self.status_bar.config(text=f"  {message}")

    def show_about(self):
        messagebox.showinfo(
            "About Blog Manager",
            "📝 Blog Post Manager v2.0\n\n"
            "A full-featured Tkinter application for\n"
            "managing blog JSON data with:\n\n"
            "• Add / Edit / Delete entries\n"
            "• Image upload & preview\n"
            "• Category presets\n"
            "• JSON import/export\n"
            "• Search & filter\n"
            "• Reorder entries\n\n"
            "Built with Python & Tkinter 🐍",
        )


# =============================================================================
# MAIN
# =============================================================================
if __name__ == "__main__":
    root = tk.Tk()

    # Set icon if available
    try:
        root.iconbitmap("icon.ico")
    except Exception:
        pass

    app = BlogManagerApp(root)
    root.mainloop()