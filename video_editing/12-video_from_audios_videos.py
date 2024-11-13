"""
This script combines multiple videos with corresponding audio files.
- Place your videos in the "12-input_video_from_audios_videos/videos" folder.
- Place matching audio files in "12-input_video_from_audios_videos/audios" folder.
- The output will be saved in "12-output_video_from_audios_videos" as 'out.mp4' (or 'out1.mp4', 'out2.mp4', etc., if 'out.mp4' already exists).

Functionality:
1. Matches each video with a corresponding audio file.
2. Adjusts video duration to match the audio, looping if necessary.
3. Fades audio in/out, and applies a fade-out effect to each video before concatenating all clips into a single output file.
"""

import os
import fnmatch
from moviepy.editor import AudioFileClip, VideoFileClip, concatenate_videoclips
import moviepy.video.fx.all as vfx
import moviepy.audio.fx.all as afx

# Constants for directories and output file
INPUT_VIDEOS_DIR = "./12-input_video_from_audios_videos/videos"
INPUT_AUDIOS_DIR = "./12-input_video_from_audios_videos/audios"
OUTPUT_DIR = "./12-output_video_from_audios_videos"
OUTPUT_FILENAME = "out.mp4"


def fetch_files(folder, extension):
    """
    Fetches files from a specified folder based on extension.
    """
    files = [os.path.join(folder, file) for file in os.listdir(folder) if fnmatch.fnmatch(file, extension)]
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


def create_video(videos, audios):
    videoclips = []

    for video, audio in zip(videos, audios):
        audio_clip = AudioFileClip(audio).fx(afx.audio_fadein, 1).fx(afx.audio_fadeout, 1)
        video_clip = VideoFileClip(video)

        if video_clip.duration < audio_clip.duration:
            video_clip = video_clip.fx(vfx.loop, duration=audio_clip.duration + 0.75)

        video_clip = video_clip.set_duration(audio_clip.duration).set_audio(audio_clip)
        videoclips.append(video_clip.fx(vfx.fadeout, 1))

    final_video = concatenate_videoclips(videoclips)
    output_path = get_unique_output_path()
    final_video.write_videofile(output_path, fps=30, remove_temp=True,
                                codec="libx264", audio_codec="aac", threads=6)


def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    videos = fetch_files(INPUT_VIDEOS_DIR, "*.mp4")
    audios = fetch_files(INPUT_AUDIOS_DIR, "*.mp3")

    if len(videos) == 0 or len(audios) == 0 or len(videos) != len(audios):
        print("Please check your input folders: ensure each video has a matching audio file.")
        return

    create_video(videos, audios)


if __name__ == "__main__":
    main()
