"""
    Video Effects Script

    This script applies various video effects to a selected input video file.
    - To use this script, place the input video in the "13-input_add_effects_to_video" directory.
    - Uncomment the desired effect within the script to apply it.
    - The output video will be saved in the "13-output_add_effects_to_video" directory with a unique name if an existing file has the same name.

    Effects options include:
    - Black and white
    - Brightness adjustment
    - Crop
    - Gamma correction
    - Freeze frame
    - Margins
    - Horizontal/Vertical flip
    - Painting effect
    - Speed change
    - Color inversion
    - Rotation
    - Supersampling
    - Luminance and contrast adjustment (default)
"""

import os
import fnmatch
from moviepy.editor import VideoFileClip
import moviepy.video.fx.all as vfx

# Constants for directories and output file
INPUT_DIR = "./13-input_add_effects_to_video"
OUTPUT_DIR = "./13-output_add_effects_to_video"
OUTPUT_FILENAME = "out.mp4"

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
        output_path = os.path.join(OUTPUT_DIR, f"out_{count}.mp4")
        count += 1
    return output_path

def apply_effects(video_path):
    """Apply selected effects to the video."""
    video_clip = VideoFileClip(video_path)
    
    # Uncomment any effect you wish to apply
    # final_video = video_clip.fx(vfx.blackwhite, RGB=None, preserve_luminosity=True)
    # final_video = video_clip.fx(vfx.colorx, 1.7)
    # final_video = video_clip.fx(vfx.crop, x1=None, y1=None, x2=None, y2=None, width=None, height=None)
    # final_video = video_clip.fx(vfx.even_size)
    # gamma_value = 0.5
    # final_video = video_clip.fx(vfx.gamma_corr, gamma_value)
    # final_video = video_clip.fx(vfx.freeze, t=3, freeze_duration=5)
    # final_video = video_clip.fx(vfx.margin, left=50, right=50, top=100, bottom=100, color=(0, 0, 0), opacity=0.2)
    # final_video = video_clip.fx(vfx.mirror_x)
    # final_video = video_clip.fx(vfx.mirror_y)
    # final_video = video_clip.fx(vfx.painting, saturation=1.4, black=0.006)
    # final_video = video_clip.fx(vfx.speedx, factor=2)
    # final_video = video_clip.fx(vfx.invert_colors)
    # final_video = video_clip.fx(vfx.rotate, 90)
    # final_video = video_clip.fx(vfx.supersample, 2, 10)
    
    # Default effect: Adjust luminance and contrast
    final_video = video_clip.fx(vfx.lum_contrast, lum=30, contrast=50)

    output_path = create_unique_output_path()
    final_video.write_videofile(output_path, fps=30, remove_temp=True, codec="libx264", audio_codec="aac", threads=6)
    video_clip.close()  # Close video resource

def main():
    video = get_video()
    if not video:
        print("Please place an MP4 video in the input directory.")
        return
    apply_effects(video)
    print("Video processing completed.")

if __name__ == "__main__":
    main()
