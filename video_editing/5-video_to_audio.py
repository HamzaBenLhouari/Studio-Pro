"""
    This script extracts audio from the first video file in the specified input directory.
    Place your video in "5-input_video_to_audio" directory,
    and the audio output will be saved in "5-output_audio" directory.
"""

import os
from moviepy.editor import VideoFileClip

INPUT_DIR = "./5-input_video_to_audio"
OUTPUT_DIR = "./5-output_audio"
OUTPUT_FILENAME = "out.mp3"

def get_video_file(directory: str) -> str:
    """Finds the first .mp4 video file in the specified directory."""
    print("Looking for video file in", directory)
    for file in os.listdir(directory):
        if file.endswith('.mp4'):
            print(f"Found video file: {file}")
            return os.path.join(directory, file)
    print("No video file found.")
    return ""

def extract_audio(video_path: str, output_path: str):
    """Extracts audio from a video file and saves it as an .mp3 file."""
    with VideoFileClip(video_path) as video:
        audio = video.audio
        audio.write_audiofile(output_path)
    print(f"Audio extracted and saved as {output_path}")

def main():
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    video_path = get_video_file(INPUT_DIR)
    if not video_path:
        print("No video to process. Exiting.")
        return
    
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)
    extract_audio(video_path, output_path)

if __name__ == "__main__":
    main()
