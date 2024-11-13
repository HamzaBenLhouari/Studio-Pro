"""
This script overlays multiple videos on a background image.
- Place your main videos in the "11-input_image_in_background" folder.
- Place a single background image in "11-input_image_in_background/bg_img" folder.
- The output will be saved in "11-output_image_in_background" as 'out.mp4' (or 'out1.mp4', 'out2.mp4', etc., if 'out.mp4' already exists).

Functionality:
1. Resizes and centers each video on top of the background image.
2. Adds a fade-in effect as each video appears sequentially.
3. Sets the background image to match the total duration of all videos.
"""

import os
import fnmatch
from moviepy.editor import ImageClip, VideoFileClip, CompositeVideoClip

# Constants for directories and output file
INPUT_VIDEOS_DIR = "./11-input_image_in_background"
INPUT_BG_IMG_DIR = "./11-input_image_in_background/bg_img"
OUTPUT_DIR = "./11-output_image_in_background"
OUTPUT_FILENAME = "out.mp4"


def get_files(folder, extensions):
    """
    Fetches files from a specified folder based on extensions.
    """
    files = []
    for file in os.listdir(folder):
        if any(fnmatch.fnmatch(file.lower(), ext) for ext in extensions):
            files.append(os.path.join(folder, file))
    return files


def get_unique_output_path():
    """
    Generates a unique output file path if the default output file already exists.
    """
    base_output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)
    output_path = base_output_path
    count = 1
    while os.path.exists(output_path):
        output_path = os.path.join(OUTPUT_DIR, f"out{count}.mp4")
        count += 1
    return output_path


def put_bg_img(videos, bg_img_path):
    img_clip = ImageClip(bg_img_path)
    video_clips = []
    end_time = 2

    for video in videos:
        clip = VideoFileClip(video).set_pos(("center", "center")).set_start(end_time).crossfadein(1)
        video_clips.append(clip)
        end_time += clip.duration + 1

    img_clip = img_clip.set_duration(end_time)

    final_video = CompositeVideoClip([img_clip, *video_clips])
    output_path = get_unique_output_path()
    final_video.write_videofile(output_path,
                                remove_temp=True,
                                codec="libx264",
                                audio_codec="aac",
                                threads=6)


def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    videos = get_files(INPUT_VIDEOS_DIR, ["*.mp4"])
    bg_imgs = get_files(INPUT_BG_IMG_DIR, ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.tiff'])

    if not videos or not bg_imgs:
        print("Check your folders: ensure both the main videos and background image are available.")
        return

    put_bg_img(videos, bg_imgs[0])


if __name__ == "__main__":
    main()
