<p align="center">
<img src="https://github.com/AryanVBW/Exif/releases/download/Exif/ExIF-Logo_BackgroundWhite.png" height="200"><br>
  A Exif-Images Edition
</p>


## Features
- Extract exif data of images jpg, jpeg, png.
- Clear exif data of images.
- Save data in a text file.
## Supported Formats
 - Images:
     - PNG, JPG, JPEG, GIF, BMP, TIFF
 - **Videos** :
     - MP4, MKV, AVI, MOV
 - **Audio** :
     - MP3 (limited support, additional library may be required)
 - OutputThe script will display metadata information for each file.If the output is set to a file, the results will be saved in exif_data.txt.
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
   pip install Pillow moviepy
   pip install eyed3
   ```

## Installation 

### Copy & paste the following commands:

```bash
git clone https://github.com/AryanVBW/Exif.git
cd Exif
python3 exif-main.py
```

### To remove exif data from images, use the following command:
```bash
python3 remove-exif.py
```
## 📸🎥🔍 direct use 

Discover the hidden details in your media files effortlessly! Simply run this script and:

  - 🌐 Enter the path to your images, videos, or audio files.
  - 💾 Choose where to save the extracted Exif data.

Unearth the metadata magic with style!
### copy paste this 
```bash
git clone https://github.com/AryanVBW/Exif.git
cd Exif
python3 exif-raw.py
```
### use this commands: for print jpg output directly on terminal or power shell 
```bash
git clone https://github.com/AryanVBW/Exif.git
cd Exif
python3 exif.py
```

### Thank You 🙏

This project was inspired by the incredible YouTube tutorial ”EXIF Data Project in Python”, which provided valuable insights into building an Exif data tool.

A heartfelt thanks to David Bombal for his fantastic exif.py script on GitHub, which served as a guiding resource during development.

To the open-source community, developers, and testers: your support makes this project thrive.

Let’s continue exploring the stories hidden within our media files!
<p align="center"> 
  Visitor count<br>
  <img src="https://profile-counter.glitch.me/Aryanvbw/count.svg" />
</p>
