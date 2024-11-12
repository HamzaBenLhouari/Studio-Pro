"""
    You don't need any input files here.
"""
from moviepy.editor import ColorClip

def create_blank_video(output_path, duration=10, fps=24, resolution=(1920, 1080), color=(255, 255, 255)):
    """
    Creates a blank video with the specified duration, frame rate, resolution, and color.

    :param output_path: Path to save the output video file.
    :param duration: Duration of the video in seconds (default is 10 seconds).
    :param fps: Frames per second (default is 24 fps).
    :param resolution: Resolution of the video as a tuple (width, height) (default is 1920x1080).
    :param color: Background color of the video as an RGB tuple (default is white).
    """
    # Create a color clip
    blank_clip = ColorClip(size=resolution, color=color, duration=duration)
    blank_clip = blank_clip.set_fps(fps)
    
    # Write the video file
    blank_clip.write_videofile(output_path, codec='libx264')

if __name__ == "__main__":
    # output path and file name
    output_path = "./1-output_create_blank_video/blank_video.mp4"
    create_blank_video(output_path)
    print(f"Blank video created and saved as {output_path}")
