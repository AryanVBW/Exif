<p align="center">
<img src="https://github.com/AryanVBW/Exif/releases/download/Exif/ExIF-Logo_BackgroundWhite.png" height="200">
  A Exif-Images Edition
</p>


## Features
- Extract exif data of images jpg, jpeg, png.
- Clear exif data of images.
- Save data in a text file.

## Please note:
This program is for .JPG and .TIFF format files. The program could be extended to support .HEIC, .PNG, and other formats.

## Installation and usage instructions:
- Add .jpg to subfolder ./images from where the script is stored. 
- Note: Most social media sites strip exif data from uploaded photos.

## Prerequisites 
1. Install python3
   - Debian, Ubuntu, Etc: `sudo apt-get install python3`
   - Fedora, Oracle, Red Hat, etc: `su -c "yum install python"`
   - Windows: [Python for Windows](https://www.python.org/downloads/windows/)

2. Install Pillow (Pillow will not work if you have PIL installed):
   ```bash 
   python3 -m pip install --upgrade pip
   python3 -m pip install --upgrade Pillow
   ```

## Installation 
### Copy & paste the following commands:
```bash
git clone https://github.com/AryanVBW/Exif.git
cd Exif
python3 exif.py
```

### To remove exif data from images, use the following command:
```bash
python3 remove-exif.py
```

