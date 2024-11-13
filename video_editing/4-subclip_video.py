import os
from moviepy.editor import VideoFileClip

INPUT_DIR = "./4-input_video"
OUTPUT_FILE = "./4-output_subclip/out.mp4"

def fetch_first_video() -> str:
    """Fetches the first MP4 video file from the input directory."""
    for file in os.listdir(INPUT_DIR):
        if file.endswith(".mp4"):
            return os.path.join(INPUT_DIR, file)
    print("No MP4 video found in the input directory.")
    return ""

def subclip_video(video_path: str, start_time: tuple = (0, 0, 3), end_time: tuple = (0, 0, 6)) -> None:
    """Creates a subclip from the input video between start and end times."""
    start_seconds = start_time[0] * 3600 + start_time[1] * 60 + start_time[2]
    end_seconds = end_time[0] * 3600 + end_time[1] * 60 + end_time[2]

    if start_seconds >= end_seconds:
        print("Error: Start time must be less than end time.")
        return

    video_clip = VideoFileClip(video_path).subclip(start_seconds, end_seconds)
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    video_clip.write_videofile(OUTPUT_FILE, fps=30, codec="libx264", audio_codec="aac", threads=6)
    print(f"Subclip saved as {OUTPUT_FILE}")

def main() -> None:
    video_path = fetch_first_video()
    if video_path:
        subclip_video(video_path)

if __name__ == "__main__":
    main()
