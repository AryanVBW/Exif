#!/usr/bin/env python3

import os
import sys
from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS
from moviepy.editor import VideoFileClip
# Add any other necessary libraries for specific formats

# Helper function
def create_google_maps_url(gps_coords):
    # Exif data stores coordinates in degree/minutes/seconds format. To convert to decimal degrees.
    dec_deg_lat = convert_decimal_degrees(float(gps_coords["lat"][0]), float(gps_coords["lat"][1]), float(gps_coords["lat"][2]), gps_coords["lat_ref"])
    dec_deg_lon = convert_decimal_degrees(float(gps_coords["lon"][0]), float(gps_coords["lon"][1]), float(gps_coords["lon"][2]), gps_coords["lon_ref"])
    return f"https://maps.google.com/?q={dec_deg_lat},{dec_deg_lon}"

def convert_decimal_degrees(degree, minutes, seconds, direction):
    decimal_degrees = degree + minutes / 60 + seconds / 3600
    if direction == "S" or direction == "W":
        decimal_degrees *= -1
    return decimal_degrees

# Print Logo
print("""                
                          /\                                                   
                         /  \   _ __ _   _  __ _ _ __                          
                        / /\ \ | '__| | | |/ _` | '_ \                         
 _ _ _ _ _ _ _ _ _ _ _ / ____ \| |  | |_| | (_| | | | |_ _ _ _ _ _ _ _ _ _ _ _ 
(_|_|_|_|_|_|_|_|_|_|_)_/    \_\_|   \__, |\__,_|_| |_(_|_|_|_|_|_|_|_|_|_|_|_)
                                      __/ |                                    
                                     |___/ by WhiteDevil 
""")

# Choice whether to keep output in the Terminal or redirect to a file.
while True:
    output_choice = input("How do you want to receive the output:\n\n1 - File\n2 - Terminal\nEnter choice here: ")
    try:
        conv_val = int(output_choice)
        if conv_val == 1:
            sys.stdout = open("exif_data.txt", "w")
            break
        elif conv_val == 2:
            break
        else:
            print("You entered an incorrect option, please try again.")
    except:
        print("You entered an invalid option, please try again.")

# Add files to the folder ./media
cwd = os.getcwd()
os.chdir(os.path.join(cwd, "media"))
files = os.listdir()

if len(files) == 0:
    print("You don't have have files in the ./media folder.")
    exit()

# Loop through the files in the media directory.
for file in files:
    try:
        file_path = os.path.join(cwd, "media", file)

        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
            media = Image.open(file_path)
            print(f"_______________________________________________________________{file}_______________________________________________________________")
            gps_coords = {}
            if media._getexif() is None:
                print(f"{file} contains no exif data.")
            else:
                for tag, value in media._getexif().items():
                    tag_name = TAGS.get(tag)
                    if tag_name == "GPSInfo":
                        for key, val in value.items():
                            print(f"{GPSTAGS.get(key)} - {val}")
                            if GPSTAGS.get(key) == "GPSLatitude":
                                gps_coords["lat"] = val
                            elif GPSTAGS.get(key) == "GPSLongitude":
                                gps_coords["lon"] = val
                            elif GPSTAGS.get(key) == "GPSLatitudeRef":
                                gps_coords["lat_ref"] = val
                            elif GPSTAGS.get(key) == "GPSLongitudeRef":
                                gps_coords["lon_ref"] = val
                    else:
                        print(f"{tag_name} - {value}")
                if gps_coords:
                    print(create_google_maps_url(gps_coords))
    except Exception as e:
        print(f"Error processing {file}: {str(e)}")

if output_choice == "1":
    sys.stdout.close()
os.chdir(cwd)
