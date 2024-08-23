#!/usr/bin/env python3

# Disclaimer: This script is for educational purposes only.
# Do not use against any photos or videos that you don't own or have authorization to test.
# ©2024 vivek w 

import os
import sys
from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS
import subprocess # For handling video files

# Helper functions (same as before)
def create_google_maps_url(gps_coords):
    # ... (unchanged)

def convert_decimal_degrees(degree, minutes, seconds, direction):
    # ... (unchanged)

# Updated logo with more information
print("""
        ██╗  ██╗ ██████╗ ██████╗ ██╗     ██╗███╗   ██╗ ██████╗ 
        ██║ ██╔╝██╔═══██╗██╔══██╗██║     ██║████╗  ██║██╔════╝ 
        █████╔╝ ██║   ██║██████╔╝██║     ██║██╔██╗ ██║██║  ███╗
        ██╔═██╗ ██║   ██║██╔══██╗██║     ██║██║╚██╗██║██║   ██║
        ██║  ██╗╚██████╔╝██║  ██║███████╗██║██║ ╚████║╚██████╔╝
        ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ 
        
        # Exif Data Extractor for Images & Videos (Educational Purposes Only)
        # Supports: JPG, TIFF, PNG, HEIC, MP4, MKV 
        # ©2024 vivek w 
""")

# Output choice (same as before)
while True:
    # ... (unchanged)

# Add files to the ./media folder (changed from ./images)
cwd = os.getcwd()
os.chdir(os.path.join(cwd, "media")) # Now looking in the "media" folder
files = os.listdir()

if len(files) == 0:
    print("No media files found in the ./media folder.")
    exit()

for file in files:
    try:
        file_extension = file.split(".")[-1].lower() # Get the file extension

        if file_extension in ["jpg", "jpeg", "tiff", "png", "heic"]:
            # Handle image files (similar to before, but now supports more formats)
            image = Image.open(file)
            print(f"\n{'_' * 80}{file}{'_' * 80}") 
            gps_coords = {}
            if image._getexif() == None:
                print(f"{file} contains no exif data.")
            else:
                for tag, value in image._getexif().items():
                    tag_name = TAGS.get(tag)
                    if tag_name == "GPSInfo":
                        # ... (same as before)
                    else:
                        print(f"{tag_name} - {value}")
                if gps_coords:
                    print(create_google_maps_url(gps_coords))

        elif file_extension in ["mp4", "mkv"]:
            # Handle video files using ffmpeg (requires ffmpeg to be installed)
            print(f"\n{'_' * 80}{file}{'_' * 80}") 
            command = f"ffmpeg -i '{file}' -map 0:2 -f ffmetadata -" # Extract metadata stream
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            metadata = result.stdout

            if "location" in metadata: # Check if GPS data exists
                location_line = [line for line in metadata.splitlines() if "location" in line][0]
                lat_lon = location_line.split("=")[1].strip("+ ") # Extract latitude and longitude
                print(f"GPS Coordinates: {lat_lon}")
                print(f"Google Maps Link: https://maps.google.com/?q={lat_lon}")
            else:
                print(f"{file} contains no GPS data.")

        else:
            print(f"File format of {file} not supported.")

    except Exception as e:
        print(f"Error processing {file}: {e}")

if output_choice == "1":
    sys.stdout.close()
os.chdir(cwd)
