from PIL import Image
from moviepy.editor import VideoFileClip
import os

def extract_image_metadata(image_path):
    try:
        with Image.open(image_path) as img:
            metadata = {
                "Format": img.format,
                "Mode": img.mode,
                "Size": img.size,
                "Info": img.info
            }
            return metadata
    except Exception as e:
        return f"Error: {str(e)}"

def extract_video_metadata(video_path):
    try:
        clip = VideoFileClip(video_path)
        metadata = {
            "Duration": clip.duration,
            "Size": os.path.getsize(video_path),
            "FPS": clip.fps,
            "Resolution": clip.size,
            "Audio": {
                "Channels": clip.audio.nchannels,
                "Sample Rate": clip.audio.fps,
                "Bit Rate": clip.audio.bitrates[0] if clip.audio.bitrates else None
            }
        }
        return metadata
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    file_path = input("Enter the path to the image or video file: ")
    if os.path.exists(file_path):
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            metadata = extract_image_metadata(file_path)
        elif file_path.lower().endswith(('.mp4', '.mkv', '.avi', '.mov', '.mp3')):
            metadata = extract_video_metadata(file_path)
        else:
            metadata = "Unsupported file format"
        
        print("Metadata:")
        print(metadata)
    else:
        print("File not found.")

if __name__ == "__main__":
    main()
