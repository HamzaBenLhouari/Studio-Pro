import os
from moviepy.editor import concatenate_videoclips, VideoFileClip

INPUT_DIR = "./2-input_concate_videos"
OUTPUT_FILE = "./2-output_concate_videos/out.mp4"

def fetch_videos() -> list[str]:
    """Fetches all .mp4 videos from the input directory."""
    videos = [os.path.join(INPUT_DIR, file) for file in os.listdir(INPUT_DIR) if file.endswith('.mp4')]
    if not videos:
        print("No videos found in the input directory.")
    return videos

def create_video_from_videos(videos: list[str]) -> None:
    """Concatenates videos and writes them to the output file."""
    clips = [VideoFileClip(video) for video in videos]
    final_clip = concatenate_videoclips(clips, method='compose')
    final_clip.write_videofile(OUTPUT_FILE, fps=30, codec="libx264", audio_codec="aac", threads=6, remove_temp=True)
    print(f"Output video saved as {OUTPUT_FILE}")

def main() -> None:
    videos = fetch_videos()
    if len(videos) < 2:
        print("Please verify: You must have more than one video to concatenate.")
        return
    create_video_from_videos(videos)

if __name__ == "__main__":
    main()
