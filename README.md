# Exif - Comprehensive Metadata Tool

<p align="center">
  <img src="https://github.com/AryanVBW/Exif/releases/download/Exif/ExIF-Logo_BackgroundWhite.png" alt="Exif Logo" height="200">
</p>

## Overview
Exif is a powerful metadata extraction tool that supports multiple file types including images, videos, audio files, and documents. It provides both a modern GUI interface and a comprehensive CLI tool for extracting detailed metadata from your files.

## Features

### 🖼️ Image Support
- Extract EXIF data from images (JPG, JPEG, PNG, GIF, BMP, TIFF)
- View image properties (dimensions, format, color profile)
- Extract GPS coordinates and view locations on Google Maps
- Remove EXIF data for privacy

### 🎥 Video Support
- Extract video metadata (duration, resolution, codec, frame rate)
- Get audio stream information
- View technical specifications

### 🎵 Audio Support
- Extract ID3 tags and audio properties
- View artist, album, and track information
- Get technical details (bitrate, sample rate, channels)

### 📄 Document Support
- Extract metadata from PDF files
- Read DOCX document properties
- View creation and modification dates

### 🌐 Location Features
- Extract GPS coordinates from images
- Generate Google Maps links
- View locations directly in your browser

## Installation

### Prerequisites
- Python 3.8 or higher
- Required libraries (install using pip):
```bash
pip install -r requirements.txt
```

### GUI Application
1. Clone the repository:
```bash
git clone https://github.com/AryanVBW/Exif.git
cd Exif
```

2. Run the GUI application:
```bash
python exif-gui.py
```

### CLI Tool
1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Basic usage:
```bash
python exif-cli.py path/to/your/file
```

3. Advanced options:
```bash
# View metadata in JSON format
python exif-cli.py path/to/your/file --format json

# Save metadata to a file
python exif-cli.py path/to/your/file --save metadata.json

# Automatically open Google Maps for location data
python exif-cli.py path/to/your/file --open-maps
```

## Supported File Types

### Images
- JPG/JPEG
- PNG
- GIF
- BMP
- TIFF

### Videos
- MP4
- AVI
- MOV
- MKV

### Audio
- MP3
- WAV
- FLAC

### Documents
- PDF
- DOC/DOCX
- TXT

## Requirements
- Python 3.8+
- Pillow
- exifread
- moviepy
- eyed3
- python-magic
- ffmpeg
- pdfplumber
- python-docx
- mutagen
- rich

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Credits
Created by AryanVBW

## Features
- Extract exif data of images jpg, jpeg, png.
- Clear exif data of images.
- Save data in a text file.
- Modern GUI application for easy metadata extraction.
- Support for multiple file types including images, videos, and audio.
## Supported Formats
 - Images:
     - PNG, JPG, JPEG, GIF, BMP, TIFF
 - **Videos** :
     - MP4, MKV, AVI, MOV
 - **Audio** :
     - MP3 (limited support, additional library may be required)
 - OutputThe script will display metadata information for each file.If the output is set to a file, the results will be saved in exif_data.txt.
## Installation and usage instructions:

### Command Line Usage
- Add .jpg to subfolder ./images from where the script is stored. 
- Note: Most social media sites strip exif data from uploaded photos.

### GUI Application Usage
1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the GUI application:
```bash
python exif-gui.py
```

3. Features of the GUI application:
   - Modern, professional interface
   - File type auto-detection
   - Support for multiple file formats
   - Save metadata to JSON or text files
   - Easy-to-use file browser
   - Detailed metadata display

## Prerequisites 
1. Install python3
   - Debian, Ubuntu, Etc: `sudo apt-get install python3`
   - Fedora, Oracle, Red Hat, etc: `su -c "yum install python"`
   - Windows: [Python for Windows](https://www.python.org/downloads/windows/)

2. Install required libraries:
   ```bash 
   python3 -m pip install --upgrade pip
   python3 -m pip install --upgrade Pillow
   pip install Pillow moviepy eyed3 python-magic
   ```

## Installation 

### Command Line Tools
```bash
git clone https://github.com/AryanVBW/Exif.git
cd Exif
python3 exif-main.py
```

### To remove exif data from images, use the following command:
```bash
python3 remove-exif.py
```
## 📸🎥🔍 Direct Use 

Discover the hidden details in your media files effortlessly! Simply run this script and:

  - 🌐 Enter the path to your images, videos, or audio files.
  - 💾 Choose where to save the extracted Exif data.

Unearth the metadata magic with style!

### Command Line Usage
```bash
git clone https://github.com/AryanVBW/Exif.git
cd Exif
python3 exif-raw.py
```

### For printing JPG output directly on terminal or PowerShell:
```bash
git clone https://github.com/AryanVBW/Exif.git
cd Exif
python3 exif.py
```

### GUI Application
For a more user-friendly experience, use the GUI application:
```bash
python exif-gui.py
```

The GUI application provides:
- 🖼️ Easy file selection
- 🔍 Auto file type detection
- 📊 Detailed metadata display
- 💾 Save options (JSON/TXT)
- 🎨 Modern, professional interface

### Thank You 🙏

This project was inspired by the incredible YouTube tutorial "[EXIF Data Project in Python](https://youtu.be/A_itRNhbgZk?si=sHaWhNV9tn4cVwWC)", which provided valuable insights into building an Exif data tool.

A heartfelt thanks to David Bombal for his fantastic [exif.py script on GitHub](https://github.com/davidbombal/red-python-scripts/blob/main/exif.py), which served as a guiding resource during development.

To the open-source community, developers, and testers: your support makes this project thrive.

Let's continue exploring the stories hidden within our media files!
<p align="center"> 
  Visitor count<br>
  <img src="https://profile-counter.glitch.me/Aryanvbw/count.svg" />
</p>
