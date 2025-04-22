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
import pdfplumber
from docx import Document
import webbrowser

class ExifMetadataGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Exif Metadata Extractor")
        self.window.geometry("1200x800")
        self.window.configure(bg="#1e1e1e")
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure(".", 
                           background="#1e1e1e",
                           foreground="#ffffff")
        self.style.configure("Treeview", 
                           background="#2d2d2d",
                           foreground="#ffffff",
                           fieldbackground="#2d2d2d")
        self.style.configure("Treeview.Heading",
                           background="#3d3d3d",
                           foreground="#ffffff")
        self.style.map("Treeview",
                      background=[('selected', '#404040')])
        
        # Configure custom styles
        self.style.configure("Custom.TFrame", background="#1e1e1e")
        self.style.configure("Custom.TLabel", 
                           background="#1e1e1e",
                           foreground="#ffffff")
        self.style.configure("Custom.TButton",
                           background="#3d3d3d",
                           foreground="#ffffff")
        self.style.configure("Custom.TLabelframe",
                           background="#2d2d2d",
                           foreground="#ffffff")
        self.style.configure("Custom.TLabelframe.Label",
                           background="#2d2d2d",
                           foreground="#ffffff")
        
        # Create main frames
        self.header_frame = ttk.Frame(self.window, style="Custom.TFrame")
        self.header_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.content_frame = ttk.Frame(self.window, style="Custom.TFrame")
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Header with logo and title
        self.logo_label = ttk.Label(self.header_frame, text="📷", 
                                  font=('Arial', 24),
                                  style="Custom.TLabel")
        self.logo_label.pack(side=tk.LEFT, padx=5)
        
        self.title_label = ttk.Label(self.header_frame, 
                                   text="Exif Metadata Extractor",
                                   font=('Arial', 18),
                                   style="Custom.TLabel")
        self.title_label.pack(side=tk.LEFT, padx=5)
        
        # Left panel for file selection and actions
        self.left_panel = ttk.Frame(self.content_frame, style="Custom.TFrame")
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # File selection
        self.file_frame = ttk.LabelFrame(self.left_panel, 
                                       text="File Selection",
                                       style="Custom.TLabelframe")
        self.file_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.file_path = tk.StringVar()
        self.file_entry = ttk.Entry(self.file_frame, 
                                  textvariable=self.file_path,
                                  width=40)
        self.file_entry.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.browse_btn = ttk.Button(self.file_frame,
                                   text="Browse",
                                   command=self.browse_file,
                                   style="Custom.TButton")
        self.browse_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Action buttons
        self.action_frame = ttk.LabelFrame(self.left_panel,
                                         text="Actions",
                                         style="Custom.TLabelframe")
        self.action_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.extract_btn = ttk.Button(self.action_frame,
                                    text="Extract Metadata",
                                    command=self.extract_metadata,
                                    style="Custom.TButton")
        self.extract_btn.pack(fill=tk.X, padx=5, pady=2)
        
        self.save_btn = ttk.Button(self.action_frame,
                                 text="Save Metadata",
                                 command=self.save_metadata,
                                 style="Custom.TButton")
        self.save_btn.pack(fill=tk.X, padx=5, pady=2)
        
        self.clear_btn = ttk.Button(self.action_frame,
                                  text="Clear",
                                  command=self.clear_display,
                                  style="Custom.TButton")
        self.clear_btn.pack(fill=tk.X, padx=5, pady=2)
        
        # Right panel for metadata display
        self.right_panel = ttk.Frame(self.content_frame, style="Custom.TFrame")
        self.right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Treeview for metadata display
        self.tree = ttk.Treeview(self.right_panel,
                               show="tree headings",
                               selectmode="browse")
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar for treeview
        self.scrollbar = ttk.Scrollbar(self.right_panel,
                                     orient="vertical",
                                     command=self.tree.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        # Footer with copyright
        self.footer_frame = ttk.Frame(self.window, style="Custom.TFrame")
        self.footer_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.copyright_label = ttk.Label(self.footer_frame,
                                       text="© 2024 Created by AryanVBW",
                                       style="Custom.TLabel")
        self.copyright_label.pack(side=tk.RIGHT)
        
        self.metadata = {}
        
    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path.set(file_path)
            
    def clear_display(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.metadata = {}
        
    def add_to_tree(self, parent, key, value):
        if isinstance(value, dict):
            item = self.tree.insert(parent, "end", text=key, open=True)
            for k, v in value.items():
                self.add_to_tree(item, k, v)
        else:
            self.tree.insert(parent, "end", text=f"{key}: {value}")
            
    def format_file_size(self, size_bytes):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.2f} TB"
        
    def get_file_info(self, file_path):
        file_info = {}
        file_stat = os.stat(file_path)
        mime = magic.Magic(mime=True)
        
        file_info["File Name"] = os.path.basename(file_path)
        file_info["File Path"] = file_path
        file_info["File Size"] = self.format_file_size(file_stat.st_size)
        file_info["File Type"] = mime.from_file(file_path)
        file_info["Created"] = datetime.fromtimestamp(file_stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
        file_info["Modified"] = datetime.fromtimestamp(file_stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        
        return file_info
        
    def extract_metadata(self):
        file_path = self.file_path.get()
        if not file_path:
            messagebox.showerror("Error", "Please select a file first!")
            return
            
        self.clear_display()
        
        try:
            # Basic file information
            self.metadata["📁 File Information"] = self.get_file_info(file_path)
            
            # Extract metadata based on file type
            mime_type = magic.Magic(mime=True).from_file(file_path)
            
            if mime_type.startswith('image/'):
                # Image metadata
                with open(file_path, 'rb') as f:
                    tags = exifread.process_file(f)
                    
                camera_info = {}
                image_props = {}
                camera_settings = {}
                timestamps = {}
                location = {}
                
                for tag, value in tags.items():
                    value_str = str(value)
                    if 'Image Make' in tag or 'Image Model' in tag:
                        camera_info[tag.split()[-1]] = value_str
                    elif 'Image ImageWidth' in tag or 'Image ImageLength' in tag:
                        image_props[tag.split()[-1]] = value_str
                    elif 'EXIF' in tag:
                        if 'DateTime' in tag:
                            timestamps[tag.split()[-1]] = value_str
                        elif 'FNumber' in tag or 'ExposureTime' in tag or 'ISOSpeedRatings' in tag:
                            camera_settings[tag.split()[-1]] = value_str
                    elif 'GPS' in tag:
                        location[tag.split()[-1]] = value_str
                        
                if camera_info:
                    self.metadata["📷 Camera Information"] = camera_info
                if image_props:
                    self.metadata["📊 Image Properties"] = image_props
                if camera_settings:
                    self.metadata["⚙️ Camera Settings"] = camera_settings
                if timestamps:
                    self.metadata["📅 Timestamps"] = timestamps
                if location:
                    self.metadata["📍 Location Data"] = location
                    
            elif mime_type.startswith('video/'):
                # Video metadata
                video = mp.VideoFileClip(file_path)
                video_info = {
                    "Duration": f"{video.duration:.2f} seconds",
                    "Resolution": f"{video.size[0]}x{video.size[1]}",
                    "FPS": f"{video.fps:.2f}",
                    "Audio": "Yes" if video.audio else "No"
                }
                self.metadata["🎥 Video Information"] = video_info
                video.close()
                
            elif mime_type.startswith('audio/'):
                # Audio metadata
                audio = eyed3.load(file_path)
                if audio.tag:
                    audio_info = {
                        "Title": audio.tag.title or "Unknown",
                        "Artist": audio.tag.artist or "Unknown",
                        "Album": audio.tag.album or "Unknown",
                        "Year": str(audio.tag.recording_date) if audio.tag.recording_date else "Unknown",
                        "Genre": audio.tag.genre.name if audio.tag.genre else "Unknown"
                    }
                    self.metadata["🎵 Audio Information"] = audio_info
                    
            elif mime_type == 'application/pdf':
                # PDF metadata
                with pdfplumber.open(file_path) as pdf:
                    pdf_info = {
                        "Pages": len(pdf.pages),
                        "Author": pdf.metadata.get('Author', 'Unknown'),
                        "Creator": pdf.metadata.get('Creator', 'Unknown'),
                        "Producer": pdf.metadata.get('Producer', 'Unknown'),
                        "Creation Date": pdf.metadata.get('CreationDate', 'Unknown')
                    }
                    self.metadata["📄 Document Information"] = pdf_info
                    
            elif mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                # DOCX metadata
                doc = Document(file_path)
                core_properties = doc.core_properties
                doc_info = {
                    "Author": core_properties.author or "Unknown",
                    "Title": core_properties.title or "Unknown",
                    "Created": str(core_properties.created) if core_properties.created else "Unknown",
                    "Modified": str(core_properties.modified) if core_properties.modified else "Unknown",
                    "Last Modified By": core_properties.last_modified_by or "Unknown"
                }
                self.metadata["📄 Document Information"] = doc_info
                
            # Display metadata in tree
            for category, data in self.metadata.items():
                category_item = self.tree.insert("", "end", text=category, open=True)
                for key, value in data.items():
                    self.add_to_tree(category_item, key, value)
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract metadata: {str(e)}")
            
    def save_metadata(self):
        if not self.metadata:
            messagebox.showerror("Error", "No metadata to save!")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.metadata, f, indent=4, ensure_ascii=False)
                messagebox.showinfo("Success", "Metadata saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save metadata: {str(e)}")
                
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = ExifMetadataGUI()
    app.run() 