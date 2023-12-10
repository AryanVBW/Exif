
<p align="center">
<img src="https://github.com/AryanVBW/kali-Linux-Android/releases/download/1/removebackground.png" height="100">
</p>
<p align="center">
<img src="https://github.com/AryanVBW/Exif/releases/download/Exif/ExIF-Logo_BackgroundWhite.png" height="200"><br>
A Exif-Images Edition
</p>

## Features
- Extract exif data of images jpg,jpeg,png.
- Clear exif data of images 
- And many more like save data in text file
## Please note: 
 This program is for .JPG and .TIFF format files. The program could be extended to support .HEIC, .PNG and other formats.
## Installation and usage instructions:
- 1. Install Pillow (Pillow will not work if you have PIL installed):
 ```bash 
  python3 -m pip install --upgrade pip
  python3 -m pip install --upgrade Pillow
 ```
- 2. Add .jpg to subfolder ./images from where the script is stored. 
- Note most social media sites strip exif data from uploaded photos.
## Prerequisites 
 - python3
    - See [installation](#Installation) for OS specifics
 - python

## Installation 
1. Install python3
 - Debian, Ubuntu, Etc
        - `sudo apt-get install python3`
 - Fedora, Oracle, Red Hat, etc
        -  `su -c "yum install python"`
 - Windows 
      -Coming soon
## copy & paste the  following commands.
```bash
 git clone https://github.com/AryanVBW/Exif.git
 cd Exif
 mkdir images
 python3 exif.py
```
