"""
    This script combines a video and background music into one output video.
    Place your video and background music in the "6-input_video_bg_m" directory,
    and the output video will be saved in "6-output_video_bg_m" directory.
"""

import os
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
import moviepy.audio.fx.all as afx

# Constants for directories and output file
INPUT_DIR = "./6-input_video_bg_m"
OUTPUT_DIR = "./6-output_video_bg_m"
OUTPUT_FILENAME = "out.mp4"

def get_first_file(directory: str, extension: str) -> str:
    """Finds the first file with the given extension in the specified directory."""
    for file in os.listdir(directory):
        if file.lower().endswith(extension):
            print(f"Found {extension} file: {file}")
            return os.path.join(directory, file)
    print(f"No {extension} file found in {directory}")
    return ""

def add_background_music(video_path: str, bg_music_path: str):
    """Adds background music to a video file."""
    with VideoFileClip(video_path) as video:
        video_duration = video.duration
        video_audio = video.audio

        try:
            bg_music = AudioFileClip(bg_music_path).volumex(0.3)  # Set volume to 30%
        except Exception as e:
            raise ValueError("Failed to load background music. Error: " + str(e))
    
        if bg_music is None:
            raise ValueError("The 'audio' clip failed to load and is None.")
    
        # if you want to start the audio in a time prefered
        """t_start = "00:01:50.35"
        t_end = None
        bg_music = bg_music.subclip(t_start,t_end)"""
        if bg_music.duration < video_duration :
                bg_music=afx.audio_loop(bg_music,duration=video_duration)

        # Combine video audio with background music, if video has audio
        final_audio = CompositeAudioClip([video_audio, bg_music]) if video_audio else bg_music
        video = video.set_audio(final_audio)

        # Ensure output directory exists
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        # Write the final video file
        output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)
        video.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac", threads=6)
        print(f"Output video with background music saved at {output_path}")


def main():
    # Get video and background music files
    video_path = get_first_file(INPUT_DIR, ".mp4")
    bg_music_path = get_first_file(INPUT_DIR, ".mp3")
    
    if not video_path:
        print("No video found. Exiting.")
        return
    if not bg_music_path:
        print("No background music found. Exiting.")
        return
    
    add_background_music(video_path, bg_music_path)

if __name__ == "__main__":
    main()