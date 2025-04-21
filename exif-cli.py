#!/usr/bin/env python3
import os
import sys
import json
import magic
import exifread
import eyed3
from PIL import Image
from datetime import datetime
from pathlib import Path
import argparse
import mimetypes
import subprocess
import ffmpeg
import pdfplumber
import docx
import mutagen
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint
import webbrowser
from rich.tree import Tree
from rich.style import Style
from rich.text import Text

class MetadataExtractor:
    def __init__(self):
        self.console = Console()
        self.mime = magic.Magic(mime=True)
        
    def convert_to_degrees(self, value):
        """Convert GPS coordinates to degrees"""
        d = float(value.values[0].num) / float(value.values[0].den)
        m = float(value.values[1].num) / float(value.values[1].den)
        s = float(value.values[2].num) / float(value.values[2].den)
        return d + (m / 60.0) + (s / 3600.0)

    def get_gps_coordinates(self, tags):
        """Extract GPS coordinates from EXIF data"""
        try:
            lat_ref = tags.get('GPS GPSLatitudeRef')
            lat = tags.get('GPS GPSLatitude')
            lon_ref = tags.get('GPS GPSLongitudeRef')
            lon = tags.get('GPS GPSLongitude')
            
            if lat and lon and lat_ref and lon_ref:
                lat_val = self.convert_to_degrees(lat)
                lon_val = self.convert_to_degrees(lon)
                
                if lat_ref.values[0] == 'S':
                    lat_val = -lat_val
                if lon_ref.values[0] == 'W':
                    lon_val = -lon_val
                
                return lat_val, lon_val
        except Exception as e:
            return None
        return None

    def get_google_maps_link(self, lat, lon):
        """Generate Google Maps link from coordinates"""
        return f"https://www.google.com/maps?q={lat},{lon}"

    def detect_file_type(self, file_path):
        """Detect file type using python-magic"""
        try:
            mime_type = self.mime.from_file(file_path)
            return mime_type
        except Exception as e:
            self.console.print(f"[red]Error detecting file type: {str(e)}[/red]")
            return None

    def get_basic_file_info(self, file_path):
        """Get basic file information"""
        file_info = {
            "File Name": os.path.basename(file_path),
            "File Path": os.path.abspath(file_path),
            "File Size": f"{os.path.getsize(file_path) / (1024*1024):.2f} MB",
            "Created": datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S'),
            "Modified": datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S'),
            "MIME Type": self.detect_file_type(file_path)
        }
        return file_info

    def extract_image_metadata(self, file_path):
        """Extract metadata from image files"""
        metadata = {}
        
        # Basic file info
        metadata.update(self.get_basic_file_info(file_path))
        
        # EXIF data
        try:
            with open(file_path, 'rb') as f:
                tags = exifread.process_file(f)
                for tag, value in tags.items():
                    if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                        metadata[tag] = str(value)
                
                # Extract GPS coordinates
                gps_coords = self.get_gps_coordinates(tags)
                if gps_coords:
                    lat, lon = gps_coords
                    metadata["GPS Latitude"] = lat
                    metadata["GPS Longitude"] = lon
                    metadata["Google Maps Link"] = self.get_google_maps_link(lat, lon)
        except Exception as e:
            metadata["EXIF Error"] = str(e)
        
        # Image properties
        try:
            with Image.open(file_path) as img:
                metadata.update({
                    "Format": img.format,
                    "Mode": img.mode,
                    "Size": f"{img.size[0]}x{img.size[1]}",
                    "DPI": img.info.get('dpi', 'N/A'),
                    "Color Profile": "Yes" if 'icc_profile' in img.info else "No"
                })
        except Exception as e:
            metadata["Image Properties Error"] = str(e)
            
        return metadata

    def extract_video_metadata(self, file_path):
        """Extract metadata from video files"""
        metadata = {}
        
        # Basic file info
        metadata.update(self.get_basic_file_info(file_path))
        
        # FFmpeg metadata
        try:
            probe = ffmpeg.probe(file_path)
            video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
            audio_info = next(s for s in probe['streams'] if s['codec_type'] == 'audio')
            
            metadata.update({
                "Duration": f"{float(probe['format']['duration']):.2f} seconds",
                "Format": probe['format']['format_name'],
                "Video Codec": video_info['codec_name'],
                "Video Resolution": f"{video_info['width']}x{video_info['height']}",
                "Frame Rate": f"{video_info['r_frame_rate']} fps",
                "Audio Codec": audio_info['codec_name'],
                "Audio Channels": audio_info['channels'],
                "Audio Sample Rate": f"{audio_info['sample_rate']} Hz",
                "Bit Rate": f"{int(probe['format']['bit_rate']) / 1000:.2f} kbps"
            })
        except Exception as e:
            metadata["FFmpeg Error"] = str(e)
            
        return metadata

    def extract_audio_metadata(self, file_path):
        """Extract metadata from audio files"""
        metadata = {}
        
        # Basic file info
        metadata.update(self.get_basic_file_info(file_path))
        
        # ID3 tags
        try:
            audio = eyed3.load(file_path)
            if audio and audio.tag:
                tag = audio.tag
                metadata.update({
                    "Title": tag.title,
                    "Artist": tag.artist,
                    "Album": tag.album,
                    "Album Artist": tag.album_artist,
                    "Track Number": tag.track_num,
                    "Year": tag.recording_date,
                    "Genre": tag.genre,
                    "Duration": f"{audio.info.time_secs:.2f} seconds",
                    "Bit Rate": f"{audio.info.bit_rate[1] / 1000:.2f} kbps",
                    "Sample Rate": f"{audio.info.sample_freq} Hz",
                    "Channels": audio.info.mode
                })
        except Exception as e:
            metadata["ID3 Error"] = str(e)
            
        # Mutagen metadata
        try:
            audio = mutagen.File(file_path)
            if audio:
                for key, value in audio.items():
                    metadata[f"Mutagen_{key}"] = str(value)
        except Exception as e:
            metadata["Mutagen Error"] = str(e)
            
        return metadata

    def extract_pdf_metadata(self, file_path):
        """Extract metadata from PDF files"""
        metadata = {}
        
        # Basic file info
        metadata.update(self.get_basic_file_info(file_path))
        
        try:
            with pdfplumber.open(file_path) as pdf:
                metadata.update({
                    "Pages": len(pdf.pages),
                    "Author": pdf.metadata.get('Author', 'N/A'),
                    "Creator": pdf.metadata.get('Creator', 'N/A'),
                    "Producer": pdf.metadata.get('Producer', 'N/A'),
                    "Subject": pdf.metadata.get('Subject', 'N/A'),
                    "Title": pdf.metadata.get('Title', 'N/A'),
                    "Creation Date": pdf.metadata.get('CreationDate', 'N/A'),
                    "Modification Date": pdf.metadata.get('ModDate', 'N/A')
                })
        except Exception as e:
            metadata["PDF Error"] = str(e)
            
        return metadata

    def extract_docx_metadata(self, file_path):
        """Extract metadata from DOCX files"""
        metadata = {}
        
        # Basic file info
        metadata.update(self.get_basic_file_info(file_path))
        
        try:
            doc = docx.Document(file_path)
            core_properties = doc.core_properties
            
            metadata.update({
                "Author": core_properties.author,
                "Category": core_properties.category,
                "Comments": core_properties.comments,
                "Content Status": core_properties.content_status,
                "Created": core_properties.created,
                "Identifier": core_properties.identifier,
                "Keywords": core_properties.keywords,
                "Language": core_properties.language,
                "Last Modified By": core_properties.last_modified_by,
                "Last Printed": core_properties.last_printed,
                "Modified": core_properties.modified,
                "Revision": core_properties.revision,
                "Subject": core_properties.subject,
                "Title": core_properties.title,
                "Version": core_properties.version
            })
        except Exception as e:
            metadata["DOCX Error"] = str(e)
            
        return metadata

    def extract_metadata(self, file_path):
        """Main method to extract metadata based on file type"""
        mime_type = self.detect_file_type(file_path)
        
        if not mime_type:
            self.console.print("[red]Could not determine file type[/red]")
            return None
            
        if mime_type.startswith('image/'):
            return self.extract_image_metadata(file_path)
        elif mime_type.startswith('video/'):
            return self.extract_video_metadata(file_path)
        elif mime_type.startswith('audio/'):
            return self.extract_audio_metadata(file_path)
        elif mime_type == 'application/pdf':
            return self.extract_pdf_metadata(file_path)
        elif mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            return self.extract_docx_metadata(file_path)
        else:
            # For unknown file types, return basic info
            return self.get_basic_file_info(file_path)

    def display_metadata(self, metadata, output_format='table'):
        """Display metadata in the specified format"""
        if output_format == 'json':
            print(json.dumps(metadata, indent=2))
        else:
            # Create a rich table
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Property", style="cyan")
            table.add_column("Value", style="green")
            
            for key, value in metadata.items():
                if key == "Google Maps Link":
                    table.add_row(str(key), f"[link={value}]{value}[/link]")
                else:
                    table.add_row(str(key), str(value))
            
            self.console.print(Panel(table, title="File Metadata", border_style="blue"))
            
            # If there's a Google Maps link, offer to open it
            if "Google Maps Link" in metadata:
                if self.console.input("\nWould you like to open the location in Google Maps? (y/n): ").lower() == 'y':
                    webbrowser.open(metadata["Google Maps Link"])

def format_file_size(size_in_bytes):
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.2f} TB"

def get_file_info(file_path):
    """Get basic file information"""
    stats = os.stat(file_path)
    return {
        "File Name": os.path.basename(file_path),
        "File Path": os.path.abspath(file_path),
        "File Size": format_file_size(stats.st_size),
        "Created": datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
        "Modified": datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
        "MIME Type": magic.from_file(file_path, mime=True)
    }

def create_metadata_table(metadata, title):
    """Create a rich table for metadata display"""
    table = Table(show_header=True, header_style="bold cyan", box=box.ROUNDED)
    table.add_column("Property", style="bold green")
    table.add_column("Value", style="yellow")
    
    for key, value in metadata.items():
        if isinstance(value, dict):
            value = json.dumps(value, indent=2)
        table.add_row(str(key), str(value))
    
    return Panel(table, title=title, border_style="blue", padding=(1, 2))

def main():
    parser = argparse.ArgumentParser(description='Extract metadata from any file type')
    parser.add_argument('file_path', help='Path to the file')
    parser.add_argument('--format', choices=['table', 'json'], default='table',
                      help='Output format (table or json)')
    parser.add_argument('--save', help='Save metadata to a JSON file')
    parser.add_argument('--open-maps', action='store_true',
                      help='Automatically open Google Maps if location data is found')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file_path):
        print(f"Error: File '{args.file_path}' not found")
        sys.exit(1)
        
    extractor = MetadataExtractor()
    metadata = extractor.extract_metadata(args.file_path)
    
    if metadata:
        extractor.display_metadata(metadata, args.format)
        
        if args.save:
            with open(args.save, 'w') as f:
                json.dump(metadata, f, indent=2)
            print(f"\nMetadata saved to {args.save}")
            
        if args.open_maps and "Google Maps Link" in metadata:
            webbrowser.open(metadata["Google Maps Link"])

if __name__ == "__main__":
    main() 