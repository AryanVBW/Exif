import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import exifread
import os
import json
from datetime import datetime
import moviepy.editor as mp
import eyed3
import magic
import io
from pathlib import Path
from ttkthemes import ThemedTk
import pdfplumber
from docx import Document
import webbrowser

class ExifGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Exif Metadata Extractor")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1e1e1e')
        
        # Set dark theme
        style = ttk.Style()
        style.theme_use('equilux')
        
        self.setup_gui()
        
    def setup_gui(self):
        # Header Frame
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Load and display logo
        try:
            logo_path = "ExIF-Logo_BackgroundWhite.png"
            logo_img = Image.open(logo_path)
            logo_img = logo_img.resize((100, 100), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = ttk.Label(header_frame, image=self.logo_photo)
            logo_label.pack(side=tk.LEFT, padx=10)
        except:
            pass
        
        title_label = ttk.Label(header_frame, 
                              text="Exif Metadata Extractor",
                              font=('Helvetica', 24, 'bold'),
                              foreground='#00ff9d')
        title_label.pack(side=tk.LEFT, padx=20)
        
        # Main Content Frame
        content_frame = ttk.Frame(self.root)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left Panel
        left_panel = ttk.Frame(content_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # File Selection
        file_frame = ttk.LabelFrame(left_panel, text="File Selection", padding=10)
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.file_path = tk.StringVar()
        path_entry = ttk.Entry(file_frame, textvariable=self.file_path, width=40)
        path_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        browse_btn = ttk.Button(file_frame, text="Browse", command=self.browse_file)
        browse_btn.pack(side=tk.LEFT)
        
        # File Type Selection
        type_frame = ttk.LabelFrame(left_panel, text="File Type", padding=10)
        type_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.file_type = tk.StringVar(value="auto")
        ttk.Radiobutton(type_frame, text="Auto Detect", value="auto", variable=self.file_type).pack(anchor=tk.W)
        ttk.Radiobutton(type_frame, text="Image", value="image", variable=self.file_type).pack(anchor=tk.W)
        ttk.Radiobutton(type_frame, text="Video", value="video", variable=self.file_type).pack(anchor=tk.W)
        ttk.Radiobutton(type_frame, text="Audio", value="audio", variable=self.file_type).pack(anchor=tk.W)
        ttk.Radiobutton(type_frame, text="Document", value="document", variable=self.file_type).pack(anchor=tk.W)
        
        # Action Buttons
        btn_frame = ttk.Frame(left_panel)
        btn_frame.pack(fill=tk.X, pady=10)
        
        extract_btn = ttk.Button(btn_frame, text="Extract Metadata", command=self.extract_metadata)
        extract_btn.pack(fill=tk.X, pady=(0, 5))
        
        save_btn = ttk.Button(btn_frame, text="Save Metadata", command=self.save_metadata)
        save_btn.pack(fill=tk.X, pady=(0, 5))
        
        clear_btn = ttk.Button(btn_frame, text="Clear", command=self.clear_display)
        clear_btn.pack(fill=tk.X)
        
        # Right Panel (Metadata Display)
        right_panel = ttk.Frame(content_frame)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create Treeview for metadata display
        self.tree = ttk.Treeview(right_panel, show='tree headings', 
                               columns=('Property', 'Value'),
                               style='Custom.Treeview')
        
        # Style the Treeview
        style.configure('Custom.Treeview',
                       background='#2d2d2d',
                       foreground='#ffffff',
                       fieldbackground='#2d2d2d',
                       rowheight=25)
        
        style.configure('Custom.Treeview.Heading',
                       background='#1e1e1e',
                       foreground='#00ff9d',
                       relief='flat')
        
        self.tree.heading('Property', text='Property')
        self.tree.heading('Value', text='Value')
        self.tree.column('Property', width=200)
        self.tree.column('Value', width=400)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(right_panel, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Footer
        footer_frame = ttk.Frame(self.root)
        footer_frame.pack(fill=tk.X, padx=20, pady=10)
        
        copyright_label = ttk.Label(footer_frame, 
                                  text="© 2024 Created by AryanVBW",
                                  foreground='#808080')
        copyright_label.pack(side=tk.RIGHT)
        
    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path.set(file_path)
            
    def clear_display(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
    def add_metadata_to_tree(self, parent, data, category=None):
        if category:
            parent = self.tree.insert(parent, 'end', text=category, values=('', ''))
            
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    self.add_metadata_to_tree(parent, value, key)
                else:
                    self.tree.insert(parent, 'end', values=(key, str(value)))
        elif isinstance(data, list):
            for i, item in enumerate(data):
                self.add_metadata_to_tree(parent, item, f"Item {i+1}")
                
    def extract_metadata(self):
        file_path = self.file_path.get()
        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("Error", "Please select a valid file.")
            return
            
        self.clear_display()
        
        try:
            # Basic file information
            file_info = {
                "File Name": os.path.basename(file_path),
                "File Path": os.path.abspath(file_path),
                "File Size": self.format_file_size(os.path.getsize(file_path)),
                "Created": datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S'),
                "Modified": datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S'),
                "MIME Type": magic.from_file(file_path, mime=True)
            }
            
            self.add_metadata_to_tree('', file_info, "📁 File Information")
            
            # Extract metadata based on file type
            mime_type = magic.from_file(file_path, mime=True)
            
            if mime_type.startswith('image/'):
                with open(file_path, 'rb') as f:
                    tags = exifread.process_file(f)
                    
                # Organize image metadata into categories
                categories = {
                    "📷 Camera Information": ["Image Make", "Image Model", "EXIF LensMake", "EXIF LensModel"],
                    "📊 Image Properties": ["EXIF ExifImageWidth", "EXIF ExifImageLength", "Image Orientation", "EXIF ColorSpace"],
                    "⚙️ Camera Settings": ["EXIF ExposureTime", "EXIF FNumber", "EXIF ISOSpeedRatings", "EXIF FocalLength"],
                    "📅 Timestamps": ["EXIF DateTimeOriginal", "EXIF DateTimeDigitized", "Image DateTime"],
                    "📍 Location": ["GPS GPSLatitude", "GPS GPSLongitude", "GPS GPSAltitude"]
                }
                
                for category, fields in categories.items():
                    category_data = {}
                    for field in fields:
                        if field in tags:
                            category_data[field] = str(tags[field])
                    if category_data:
                        self.add_metadata_to_tree('', category_data, category)
                        
            elif mime_type.startswith('video/'):
                video = mp.VideoFileClip(file_path)
                video_info = {
                    "Duration": f"{video.duration:.2f} seconds",
                    "FPS": video.fps,
                    "Size": f"{video.size[0]}x{video.size[1]}",
                    "Audio": "Yes" if video.audio else "No"
                }
                self.add_metadata_to_tree('', video_info, "🎥 Video Information")
                video.close()
                
            elif mime_type.startswith('audio/'):
                audio = eyed3.load(file_path)
                if audio and audio.tag:
                    audio_info = {
                        "Title": audio.tag.title,
                        "Artist": audio.tag.artist,
                        "Album": audio.tag.album,
                        "Year": audio.tag.recording_date,
                        "Genre": audio.tag.genre,
                        "Bitrate": f"{audio.info.bit_rate[1]}kbps",
                        "Sample Rate": f"{audio.info.sample_freq}Hz",
                        "Duration": f"{audio.info.time_secs:.2f} seconds"
                    }
                    self.add_metadata_to_tree('', audio_info, "🎵 Audio Information")
                    
            elif mime_type == 'application/pdf':
                with pdfplumber.open(file_path) as pdf:
                    pdf_info = {
                        "Number of Pages": len(pdf.pages),
                        "Author": pdf.metadata.get('Author', 'N/A'),
                        "Creator": pdf.metadata.get('Creator', 'N/A'),
                        "Producer": pdf.metadata.get('Producer', 'N/A'),
                        "Creation Date": pdf.metadata.get('CreationDate', 'N/A'),
                        "Modification Date": pdf.metadata.get('ModDate', 'N/A')
                    }
                    self.add_metadata_to_tree('', pdf_info, "📄 PDF Information")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract metadata: {str(e)}")
            
    def save_metadata(self):
        metadata = {}
        for item in self.tree.get_children():
            category = self.tree.item(item)['text']
            metadata[category] = {}
            for child in self.tree.get_children(item):
                values = self.tree.item(child)['values']
                if values:
                    metadata[category][values[0]] = values[1]
                    
        if metadata:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("Text files", "*.txt")]
            )
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("Success", "Metadata saved successfully!")
                
    def format_file_size(self, size_in_bytes):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_in_bytes < 1024.0:
                return f"{size_in_bytes:.2f} {unit}"
            size_in_bytes /= 1024.0
        return f"{size_in_bytes:.2f} TB"

def main():
    root = ThemedTk(theme="equilux")
    app = ExifGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 