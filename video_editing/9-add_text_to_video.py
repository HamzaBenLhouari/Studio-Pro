"""
    You Need Input Files Here (Video and Text File)
    - Place your video file and a text file (containing the desired text) in the "9-input_add_text_to_video" directory.
    - The script will generate a new video with the specified text overlay in the "9-output_add_text_to_video" directory.

    How This Script Works:
    - Finds the first video and text file in the input directory (.mp4 for the video, .txt for the text file).
    - Reads the text from the file and overlays it at the center of the video for a duration of 10 seconds.
    - The final video will be saved as "out.mp4" in the output directory.
    
    Customization:
    - To adjust text position, duration, font, color, and size, edit the parameters in the script.
    - If "out.mp4" already exists, the script will create additional output files with incremental names like "out1.mp4", "out2.mp4", etc.
    
    
    if an error has occured read what's writen in the end of this file
"""

import os
import fnmatch
from moviepy.editor import TextClip, VideoFileClip, CompositeVideoClip
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": "C:/Program Files/ImageMagick-7.1.1-Q16-HDRI/magick.exe"})

# Constants for directories and output file
INPUT_DIR = "./9-input_add_text_to_video"
OUTPUT_DIR = "./9-output_add_text_to_video"
OUTPUT_FILENAME = "out.mp4"

def get_file(extension):
    """Fetches the first file with the given extension in the input directory."""
    for file in os.listdir(INPUT_DIR):
        if fnmatch.fnmatch(file.lower(), extension):
            return os.path.join(INPUT_DIR, file)
    return ""

def generate_video(text, video_path):
    """Generates a video with centered text overlay."""
    clip = VideoFileClip(video_path)
    txt_clip = TextClip(text, font='DejaVu-Sans-Mono-Bold', fontsize=75, color='black')
    txt_clip = txt_clip.set_pos('center').set_duration(10)
    
    final_video = CompositeVideoClip([clip, txt_clip])
    
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)
    index = 1
    while os.path.exists(output_path):
        output_path = os.path.join(OUTPUT_DIR, f"out{index}.mp4")
        index += 1
    
    final_video.write_videofile(output_path, audio_codec='aac', threads=6)

def get_content(file_path):
    """Reads content from a text file."""
    with open(file_path) as f:
        return f.read().strip()

def main():
    video_path = get_file('*.mp4')
    text_file_path = get_file('*.txt')
    
    if not video_path or not text_file_path:
        print("Missing video or text file in the input directory.")
        return
    
    text = get_content(text_file_path)
    if not text:
        print("Text file is empty.")
        return
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    generate_video(text, video_path)

if __name__ == "__main__":
    main()


"""
error message : 
##########
OSError: MoviePy Error: creation of None failed because of the following error:

[WinError 2] Le fichier spécifié est introuvable.

.This error can be due to the fact that ImageMagick is not installed 
on your computer, or (for Windows users) that you didn't specify the 
path to the ImageMagick binary in file conf.py, or that the path you 
specified is incorrect
##############"
This error message from MoviePy typically occurs when the program tries to use ImageMagick for handling text clips (like creating text overlay) but can't locate the ImageMagick binary. Here are the steps you can take to resolve this:

Install ImageMagick:

Download and install ImageMagick from the official website.
During installation, ensure that you select the option to add ImageMagick to your system PATH (this option may appear as "Add application directory to your system path").
Configure MoviePy:

After installation, MoviePy may need the path to the magick binary in its configuration.

Locate where magick.exe was installed (usually in C:\Program Files\ImageMagick or C:\Program Files (x86)\ImageMagick).

In your Python script, set the path to ImageMagick explicitly:

python
Copier le code
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": "C:/path/to/magick.exe"})
Replace "C:/path/to/magick.exe" with the actual path to magick.exe.

"""