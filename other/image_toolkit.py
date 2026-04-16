#
# --- Tkinter Image Toolkit ---
#
# A complete desktop application for batch image processing.
# Features: Convert, Compress, Crop, Rename, and Paste-from-Clipboard.
#
# Coded by: A helpful AI Assistant
# Version: 1.0
#

import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageGrab, ImageTk, ImageOps
import os
import io

# --- Main Application Class ---
class ImageToolkitApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.title("Tkinter Image Toolkit")
        self.geometry("1200x700")
        self.minsize(1000, 600)
        ctk.set_appearance_mode("dark")

        # --- App State Variables ---
        self.image_files = [] # List to hold info about each image
        self.current_image_index = None
        self.original_pil_image = None # Unmodified PIL image
        self.processed_pil_image = None # Image after crop/resize
        self.display_photo_image = None # CTkImage for display

        # Cropping state
        self.crop_start_x = None
        self.crop_start_y = None
        self.crop_rect_id = None

        # --- UI Layout (3-Column Grid) ---
        self.grid_columnconfigure(0, weight=1) # File List
        self.grid_columnconfigure(1, weight=3) # Image Preview
        self.grid_columnconfigure(2, weight=1) # Controls
        self.grid_rowconfigure(0, weight=1)

        # --- Create UI Frames ---
        self.create_file_list_frame()
        self.create_image_preview_frame()
        self.create_controls_frame()

        # --- Bindings ---
        self.bind("<Control-v>", self.paste_from_clipboard)

    # --- UI Creation Methods ---

    def create_file_list_frame(self):
        self.file_list_frame = ctk.CTkScrollableFrame(self, label_text="Image Files")
        self.file_list_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    def create_image_preview_frame(self):
        self.preview_frame = ctk.CTkFrame(self)
        self.preview_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.preview_frame.grid_rowconfigure(0, weight=1)
        self.preview_frame.grid_columnconfigure(0, weight=1)

        self.preview_label = ctk.CTkLabel(self.preview_frame, text="Select a folder or paste an image (Ctrl+V)")
        self.preview_label.grid(row=0, column=0, sticky="nsew")

        # Canvas for cropping, placed on top of the label
        self.crop_canvas = ctk.CTkCanvas(self.preview_frame, bg="gray15", highlightthickness=0)
        self.crop_canvas.bind("<ButtonPress-1>", self.on_crop_start)
        self.crop_canvas.bind("<B1-Motion>", self.on_crop_drag)
        self.crop_canvas.bind("<ButtonRelease-1>", self.on_crop_end)

    def create_controls_frame(self):
        self.controls_frame = ctk.CTkFrame(self)
        self.controls_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        # Folder/File Buttons
        folder_button = ctk.CTkButton(self.controls_frame, text="Select Folder", command=self.select_folder)
        folder_button.pack(pady=10, padx=10, fill="x")

        paste_button = ctk.CTkButton(self.controls_frame, text="Paste from Clipboard", command=self.paste_from_clipboard)
        paste_button.pack(pady=5, padx=10, fill="x")

        # --- Conversion Settings ---
        conversion_label = ctk.CTkLabel(self.controls_frame, text="Conversion", font=ctk.CTkFont(weight="bold"))
        conversion_label.pack(pady=(20, 5), padx=10, anchor="w")

        self.format_var = ctk.StringVar(value="WebP")
        format_menu = ctk.CTkOptionMenu(self.controls_frame, values=["WebP", "PNG", "JPEG"], variable=self.format_var, command=self.update_estimated_size)
        format_menu.pack(pady=5, padx=10, fill="x")

        quality_label = ctk.CTkLabel(self.controls_frame, text="Quality (for WebP/JPEG): 85")
        quality_label.pack(pady=5, padx=10, anchor="w")
        self.quality_slider = ctk.CTkSlider(self.controls_frame, from_=0, to=100, number_of_steps=100, command=lambda val: self.update_quality_label(val))
        self.quality_slider.set(85)
        self.quality_slider.pack(pady=5, padx=10, fill="x")

        self.estimated_size_label = ctk.CTkLabel(self.controls_frame, text="Est. Size: N/A", text_color="gray")
        self.estimated_size_label.pack(pady=5, padx=10, anchor="w")

        # --- Cropping Controls ---
        crop_label = ctk.CTkLabel(self.controls_frame, text="Crop", font=ctk.CTkFont(weight="bold"))
        crop_label.pack(pady=(20, 5), padx=10, anchor="w")
        
        crop_info = ctk.CTkLabel(self.controls_frame, text="Drag on image to crop", text_color="gray")
        crop_info.pack(pady=5, padx=10, anchor="w")

        reset_crop_button = ctk.CTkButton(self.controls_frame, text="Reset Crop", command=self.reset_crop)
        reset_crop_button.pack(pady=5, padx=10, fill="x")

        # --- Renaming ---
        rename_label = ctk.CTkLabel(self.controls_frame, text="Batch Rename", font=ctk.CTkFont(weight="bold"))
        rename_label.pack(pady=(20, 5), padx=10, anchor="w")
        self.prefix_entry = ctk.CTkEntry(self.controls_frame, placeholder_text="Prefix")
        self.prefix_entry.pack(pady=5, padx=10, fill="x")
        self.suffix_entry = ctk.CTkEntry(self.controls_frame, placeholder_text="Suffix")
        self.suffix_entry.pack(pady=5, padx=10, fill="x")

        # --- Final Action Button ---
        process_button = ctk.CTkButton(self.controls_frame, text="Process & Save All", command=self.process_and_save, height=40)
        process_button.pack(pady=(30, 10), padx=10, fill="x", side="bottom")

    # --- Core Functionality Methods ---

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if not folder_path:
            return

        self.image_files.clear()
        self.current_image_index = None
        self.clear_ui()

        valid_extensions = (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff")
        for filename in sorted(os.listdir(folder_path)):
            if filename.lower().endswith(valid_extensions):
                self.image_files.append({"path": os.path.join(folder_path, filename), "crop": None})

        self.update_file_list_ui()
        if self.image_files:
            self.select_image(0)

    def paste_from_clipboard(self, event=None):
        try:
            pasted_image = ImageGrab.grabclipboard()
            if isinstance(pasted_image, Image.Image):
                # We have an image!
                if self.current_image_index is None: # Clear list if it's empty
                    self.image_files.clear()
                
                new_image_entry = {"path": "<Clipboard>", "crop": None, "pil_image": pasted_image}
                self.image_files.append(new_image_entry)
                
                self.update_file_list_ui()
                self.select_image(len(self.image_files) - 1)
            else:
                # The clipboard doesn't contain a standard image
                messagebox.showinfo("Info", "No image found on the clipboard.")
        except Exception:
            # On some systems, this can fail if clipboard is empty or not an image
            messagebox.showinfo("Info", "Could not get image from clipboard.")

    def select_image(self, index):
        self.current_image_index = index
        self.reset_crop() # Reset crop when selecting a new image

        image_info = self.image_files[index]
        if "pil_image" in image_info: # It's a pasted image
            self.original_pil_image = image_info["pil_image"].copy()
        else: # It's a file
            self.original_pil_image = Image.open(image_info["path"])

        self.update_preview()
        self.update_estimated_size()

    def update_preview(self):
        if not self.original_pil_image:
            return

        # Apply crop if it exists
        if self.image_files[self.current_image_index].get("crop"):
            crop_box = self.image_files[self.current_image_index]["crop"]
            self.processed_pil_image = self.original_pil_image.crop(crop_box)
        else:
            self.processed_pil_image = self.original_pil_image.copy()

        # Fit image to the preview frame for display
        frame_w = self.preview_frame.winfo_width()
        frame_h = self.preview_frame.winfo_height()
        if frame_w < 50 or frame_h < 50: # Frame not ready yet
            self.after(50, self.update_preview)
            return

        display_image = self.processed_pil_image.copy()
        
        # Add checkerboard for transparent images
        if display_image.mode in ('RGBA', 'LA') or (display_image.mode == 'P' and 'transparency' in display_image.info):
            checkerboard = self.create_checkerboard(display_image.width, display_image.height)
            checkerboard.paste(display_image, (0, 0), display_image)
            display_image = checkerboard

        display_image.thumbnail((frame_w - 20, frame_h - 20), Image.Resampling.LANCZOS)
        
        self.display_photo_image = ctk.CTkImage(light_image=display_image, dark_image=display_image, size=display_image.size)
        self.preview_label.configure(image=self.display_photo_image, text="")

        # Place canvas over the label, matching its size
        self.crop_canvas.place(x=self.preview_label.winfo_x(), y=self.preview_label.winfo_y(),
                               width=self.display_photo_image.cget("size")[0],
                               height=self.display_photo_image.cget("size")[1])

    def update_estimated_size(self, _=None):
        if not self.processed_pil_image:
            self.estimated_size_label.configure(text="Est. Size: N/A")
            return

        try:
            img_format = self.format_var.get().lower()
            quality = int(self.quality_slider.get())
            buffer = io.BytesIO()

            save_params = {}
            if img_format in ["webp", "jpeg"]:
                save_params['quality'] = quality
                
            # Use RGB mode for formats that don't support RGBA
            image_to_save = self.processed_pil_image
            if img_format == "jpeg" and image_to_save.mode == 'RGBA':
                image_to_save = image_to_save.convert('RGB')
                
            image_to_save.save(buffer, format=img_format, **save_params)
            size_kb = len(buffer.getvalue()) / 1024
            self.estimated_size_label.configure(text=f"Est. Size: {size_kb:.1f} KB")
        except Exception as e:
            self.estimated_size_label.configure(text="Est. Size: Error")
            print(f"Error estimating size: {e}")

    # --- UI Update Methods ---

    def update_file_list_ui(self):
        # Clear old widgets
        for widget in self.file_list_frame.winfo_children():
            widget.destroy()

        for i, img_info in enumerate(self.image_files):
            filename = os.path.basename(img_info['path'])
            btn = ctk.CTkButton(self.file_list_frame, text=filename, fg_color="transparent",
                                command=lambda i=i: self.select_image(i))
            btn.pack(fill="x", padx=5)
            if i == self.current_image_index:
                btn.configure(fg_color="gray25")

    def update_quality_label(self, value):
        value = int(value)
        self.controls_frame.winfo_children()[4].configure(text=f"Quality (for WebP/JPEG): {value}")
        self.update_estimated_size()
    
    def clear_ui(self):
        self.preview_label.configure(image=None, text="Select a folder or paste an image (Ctrl+V)")
        self.estimated_size_label.configure(text="Est. Size: N/A")
        self.update_file_list_ui()

    # --- Cropping Methods ---

    def on_crop_start(self, event):
        self.crop_start_x = event.x
        self.crop_start_y = event.y
        if self.crop_rect_id:
            self.crop_canvas.delete(self.crop_rect_id)
        self.crop_rect_id = self.crop_canvas.create_rectangle(self.crop_start_x, self.crop_start_y, self.crop_start_x, self.crop_start_y, outline='cyan', width=2)

    def on_crop_drag(self, event):
        if self.crop_rect_id:
            self.crop_canvas.coords(self.crop_rect_id, self.crop_start_x, self.crop_start_y, event.x, event.y)

    def on_crop_end(self, event):
        if self.crop_start_x is None: return

        # Get canvas coordinates
        c_x1, c_y1, c_x2, c_y2 = self.crop_canvas.coords(self.crop_rect_id)
        
        # Get displayed image size and original processed image size
        disp_w, disp_h = self.display_photo_image.cget("size")
        orig_w, orig_h = self.processed_pil_image.size

        # Translate canvas coordinates to original image coordinates
        scale_x = orig_w / disp_w
        scale_y = orig_h / disp_h
        
        img_x1 = int(min(c_x1, c_x2) * scale_x)
        img_y1 = int(min(c_y1, c_y2) * scale_y)
        img_x2 = int(max(c_x1, c_x2) * scale_x)
        img_y2 = int(max(c_y1, c_y2) * scale_y)

        # Ensure crop box is valid
        if img_x2 > img_x1 and img_y2 > img_y1:
            self.image_files[self.current_image_index]["crop"] = (img_x1, img_y1, img_x2, img_y2)
            self.update_preview()
            self.update_estimated_size()
        
        self.crop_start_x = self.crop_start_y = None
    
    def reset_crop(self):
        if self.current_image_index is not None:
            self.image_files[self.current_image_index]["crop"] = None
            if self.crop_rect_id:
                self.crop_canvas.delete(self.crop_rect_id)
                self.crop_rect_id = None
            self.update_preview()
            self.update_estimated_size()

    # --- Utility Methods ---

    @staticmethod
    def create_checkerboard(width, height, square_size=10):
        board = Image.new('RGB', (width, height), '#808080')
        pixels = board.load()
        for x in range(width):
            for y in range(height):
                if (x // square_size) % 2 == (y // square_size) % 2:
                    pixels[x, y] = (192, 192, 192) # Light gray
        return board

    # --- Main Processing Method ---
    def process_and_save(self):
        if not self.image_files:
            messagebox.showwarning("Warning", "No images loaded to process.")
            return

        output_folder = filedialog.askdirectory(title="Select Output Folder")
        if not output_folder:
            return

        prefix = self.prefix_entry.get()
        suffix = self.suffix_entry.get()
        img_format = self.format_var.get().lower()
        quality = int(self.quality_slider.get())

        processed_count = 0
        try:
            for i, img_info in enumerate(self.image_files):
                # Load original image
                if "pil_image" in img_info:
                    img = img_info["pil_image"].copy()
                    base_name = f"clipboard_image_{i}"
                else:
                    img = Image.open(img_info["path"])
                    base_name, _ = os.path.splitext(os.path.basename(img_info["path"]))

                # Apply crop
                if img_info.get("crop"):
                    img = img.crop(img_info["crop"])

                # Create new filename
                new_filename = f"{prefix}{base_name}{suffix}.{img_format}"
                output_path = os.path.join(output_folder, new_filename)
                
                # Prepare save parameters
                save_params = {}
                if img_format in ["webp", "jpeg"]:
                    save_params['quality'] = quality

                # Convert to RGB if saving as JPEG and image has alpha
                if img_format == "jpeg" and img.mode == 'RGBA':
                    img = img.convert('RGB')
                
                # Save the image
                img.save(output_path, **save_params)
                processed_count += 1
            
            messagebox.showinfo("Success", f"Successfully processed and saved {processed_count} images to:\n{output_folder}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during processing:\n{e}")


if __name__ == "__main__":
    app = ImageToolkitApp()
    app.mainloop()