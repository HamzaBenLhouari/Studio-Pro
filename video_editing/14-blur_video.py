"""
    Blur Video Effect Script

    This script applies a Gaussian blur effect to all frames in a video file. 
    To use this script:
    - Place the input video in the "14-input_blur_video" directory.
    - The output video will be saved in the "14-output_blur_video" directory.

    If an output file with the same name already exists, a new file will be created with an incremented name.
"""

import os
import fnmatch
from moviepy.editor import VideoFileClip
from PIL import Image, ImageFilter
import numpy as np

# Constants for directories and output file
INPUT_DIR = "./14-input_blur_video"
OUTPUT_DIR = "./14-output_blur_video"
OUTPUT_FILENAME = "blurred_video.mp4"

def get_video():
    """Fetch the first MP4 video file from the input directory."""
    print("Getting video...")
    for file in os.listdir(INPUT_DIR):
        if fnmatch.fnmatch(file.lower(), '*.mp4'):
            video_path = os.path.join(INPUT_DIR, file)
            print(f"Video found: {file}")
            return video_path
    print("No video found in the input directory.")
    return ""

def create_unique_output_path():
    """Generate a unique output path if the output file already exists."""
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)
    count = 1
    while os.path.exists(output_path):
        output_path = os.path.join(OUTPUT_DIR, f"blurred_video_{count}.mp4")
        count += 1
    return output_path

def blur_frame(image_frame):
    """Apply Gaussian blur to a video frame."""
    pil_image = Image.fromarray(image_frame)
    blurred_image = pil_image.filter(ImageFilter.GaussianBlur(radius=5))
    return np.array(blurred_image)

def blur_video(video_path):
    """Apply blur effect to each frame of the video and save it."""
    clip = VideoFileClip(video_path)
    blurred_clip = clip.fl_image(blur_frame)
    output_path = create_unique_output_path()
    blurred_clip.write_videofile(output_path, fps=clip.fps, codec="libx264", audio_codec="aac")
    clip.close()  # Close the clip to release resources

def main():
    video = get_video()
    if not video:
        print("Please place an MP4 video in the input directory.")
        return
    blur_video(video)
    print("Video processing completed.")

if __name__ == "__main__":
    main()
