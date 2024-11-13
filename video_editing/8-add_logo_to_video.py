"""
    You Need Input Files Here (Video and Logo Image)
    Put your video and logo image in the "8-input-add_logo_to_video" directory
    and wait for the output video with logo in the "8-output-add_logo_to_video" directory.
    
    What this script does:
    - It finds the first video and logo image from the input directory
      (supports video format .mp4 and common image formats like .jpg, .png, etc.).
    - Adds the logo to the top-right corner of the video, with optional padding and resizing.
    - Saves the final video in the output directory with the name "out.mp4".
    - If "out.mp4" already exists, the script will automatically name the new file "out1.mp4", "out2.mp4", etc.

    Adjustments:
    - You can customize the logo position, padding, and size by editing the parameters in the script.
"""
import os
import fnmatch
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

# Constants for directories and output file
INPUT_DIR = "./8-input-add_logo_to_video"
OUTPUT_DIR = "./8-output-add_logo_to_video"
OUTPUT_FILENAME = "out.mp4"

def get_file(extensions):
    """
    Fetches the first file that matches the given extensions from the input directory.
    """
    print("Searching for files...")
    for file in os.listdir(INPUT_DIR):
        if any(fnmatch.fnmatch(file.lower(), ext) for ext in extensions):
            print(f"Found file: {file}")
            return os.path.join(INPUT_DIR, file)
    print("No matching file found.")
    return ""

def generate_output_filename(base_name):
    """
    Generates a unique filename in the output directory if the file already exists.
    """
    filename = os.path.join(OUTPUT_DIR, base_name)
    count = 1
    while os.path.exists(filename):
        filename = os.path.join(OUTPUT_DIR, f"out{count}.mp4")
        count += 1
    return filename

def add_logo_to_video(logo_path, video_path):
    """
    Adds the logo to the top-right corner of the video and saves it.
    """
    clip = VideoFileClip(video_path)

    logo = (ImageClip(logo_path)
            .set_duration(clip.duration)
            #.resize(height=50)  # Uncomment to resize the logo if needed
            .margin(right=8, top=8, opacity=0)  # Adds optional padding for the logo
            .set_pos(("right", "top")))

    final = CompositeVideoClip([clip, logo])
    
    output_path = generate_output_filename(OUTPUT_FILENAME)
    print(f"Saving output video to {output_path}")
    final.write_videofile(output_path, fps=30, remove_temp=True,
                          codec="libx264", audio_codec="aac", threads=6)

def main():
    logo = get_file(['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.tiff'])
    video = get_file(['*.mp4'])
    
    if not logo or not video:
        print("Logo or video file is missing. Please add the necessary files.")
        return

    add_logo_to_video(logo, video)

if __name__ == "__main__":
    main()
