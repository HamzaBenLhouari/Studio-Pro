"""
This script overlays a series of videos on a background video.
- Place your main videos in the "10-input_video_in_background" folder.
- Place a single background video in "10-input_video_in_background/bg_video" folder.
- The output will be saved in "10-output_video_in_background" as 'out.mp4' (or 'out1.mp4', 'out2.mp4', etc., if 'out.mp4' already exists).

Functionality:
1. The script automatically resizes and centers each input video over the background.
2. Each video is added sequentially, with a fade-in effect between them.
3. If the combined duration of the input videos exceeds the background video length, 
   the background will loop to match the total duration.
"""

import os
import fnmatch
from moviepy.editor import VideoFileClip, CompositeVideoClip
import moviepy.video.fx.all as vfx

# Constants for directories and output file
INPUT_VIDEOS_DIR = "./10-input_video_in_background"
INPUT_BG_VIDEO_DIR = "./10-input_video_in_background/bg_video"
OUTPUT_DIR = "./10-output_video_in_background"
OUTPUT_FILENAME = "out.mp4"


def fetch_videos(folder, extensions="*.mp4"):
    """
    Fetches video files from a specified folder based on extension.
    """
    videos = []
    for file in os.listdir(folder):
        if fnmatch.fnmatch(file, extensions):
            videos.append(os.path.join(folder, file))
    return videos


def get_unique_output_path():
    """
    Generates a unique output file path by adding an incremental number
    if the default output file already exists.
    """
    base_output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)
    output_path = base_output_path
    count = 1
    while os.path.exists(output_path):
        output_path = os.path.join(OUTPUT_DIR, f"out{count}.mp4")
        count += 1
    return output_path


def put_bg_video(videos, bg_video_path):
    bg_video = VideoFileClip(bg_video_path)
    video_clips = []
    end_time = 2

    for video in videos:
        clip = VideoFileClip(video)
        clip = clip.set_pos(("center", "center")).set_start(end_time).crossfadein(1)
        video_clips.append(clip)
        end_time += clip.duration + 1

    if bg_video.duration < end_time:
        bg_video = bg_video.fx(vfx.loop, duration=end_time)
    else:
        bg_video = bg_video.subclip(0, end_time)

    final_video = CompositeVideoClip([bg_video, *video_clips])
    output_path = get_unique_output_path()
    final_video.write_videofile(output_path,
                                remove_temp=True,
                                codec="libx264",
                                audio_codec="aac",
                                threads=6)


def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    videos = fetch_videos(INPUT_VIDEOS_DIR)
    bg_video_files = fetch_videos(INPUT_BG_VIDEO_DIR)
    
    if not videos or not bg_video_files:
        print("Check your video folders: make sure both the main videos and background video are available.")
        return
    
    put_bg_video(videos, bg_video_files[0])


if __name__ == "__main__":
    main()
