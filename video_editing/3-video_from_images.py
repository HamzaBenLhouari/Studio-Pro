import os
from moviepy.editor import concatenate_videoclips, ImageClip

INPUT_DIR = "./3-input_video_from_images"
OUTPUT_FILE = "./3-output_video_from_images/out.mp4"
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}

def fetch_images() -> list[str]:
    """Fetches all images from the input directory with specified extensions."""
    images = [os.path.join(INPUT_DIR, file) for file in os.listdir(INPUT_DIR)
              if any(file.lower().endswith(ext) for ext in IMAGE_EXTENSIONS)]
    if not images:
        print("No images found in the input directory.")
    return images

def create_video_from_images(images: list[str], duration: int = 2, crossfade_duration: int = 1) -> None:
    """Creates a video from images, applying crossfade transitions."""
    clips = [ImageClip(img).set_duration(duration) for img in images]
    clips = [clips[i].crossfadein(crossfade_duration) for i in range(len(clips))]
    video = concatenate_videoclips(clips, method="compose")
    
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    video.write_videofile(OUTPUT_FILE, fps=24, codec="libx264")
    print(f"Output video saved as {OUTPUT_FILE}")

def main() -> None:
    images = fetch_images()
    if len(images) < 2:
        print("Please verify: You must have more than one image.")
        return
    create_video_from_images(images)

if __name__ == "__main__":
    main()
