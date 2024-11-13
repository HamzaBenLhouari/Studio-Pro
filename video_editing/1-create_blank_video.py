from moviepy.editor import ColorClip

def create_blank_video(
    output_path: str = "./1-output_create_blank_video/blank_video.mp4", 
    duration: int = 10, 
    fps: int = 24, 
    resolution: tuple[int, int] = (1920, 1080), 
    color: tuple[int, int, int] = (255, 255, 255)
) -> None:
    """
    Creates a blank video with specified duration, frame rate, resolution, and color.
    """
    blank_clip = ColorClip(size=resolution, color=color, duration=duration).set_fps(fps)
    blank_clip.write_videofile(output_path, codec='libx264')
    print(f"Blank video created and saved as {output_path}")

if __name__ == "__main__":
    create_blank_video()
