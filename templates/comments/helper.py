from moviepy.editor import AudioFileClip, VideoFileClip, ImageClip, CompositeVideoClip, CompositeAudioClip
import moviepy.video.fx.all as vfx
import moviepy.audio.fx.all as afx
import fnmatch
import os
from PIL import Image

def get_comments():
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.tiff']
    images = []
    
    # Check if the comments directory exists
    comments_dir = os.path.join('.', 'comments')
    if not os.path.exists(comments_dir):
        print("Error: './comments' directory not found.")
        return images
    
    # Get and sort files in the comments directory
    files = os.listdir(comments_dir)
    sorted_files = sorted(files)

    # Filter and add image files to the list
    for file in sorted_files:
        if any(fnmatch.fnmatch(file.lower(), ext) for ext in image_extensions):
            images.append(os.path.join(comments_dir, file))
    
    # Print message if no images found
    if not images:
        print("Images not found")
    else:
        print("Images done")
    
    return images

def get_audios():
    print("Getting audios...")
    audios = []
    
    # Define the directory path
    audios_dir = os.path.join('.', 'audios')
    
    # Check if the directory exists
    if not os.path.exists(audios_dir):
        print("Error: './audios' directory not found.")
        return audios

    # Get and sort files in the audios directory
    files = os.listdir(audios_dir)
    sorted_files = sorted(files)

    # Filter and add audio files to the list
    for file in sorted_files:
        if fnmatch.fnmatch(file.lower(), '*.mp3'):
            print(file)
            audios.append(os.path.join(audios_dir, file))
    
    # Print message if no audio files found
    if not audios:  # This checks if the list is empty
        print("Audios not found")
    else:
        print("Audios retrieved successfully")
    
    return audios

def generate_video():
    # Fetch images and audios
    images = get_comments()
    audios = get_audios()

    # Verify if images and audios lists are valid
    if not images or not audios or len(images) != len(audios):
        print("Verify your files, please!")
        return

    audio_clips = []
    image_clips = []

    # Get background video
    bg_video = get_bg('*.mp4')
    if not bg_video:
        print("No background video file found.")
        return
    video_Clip = VideoFileClip(bg_video)

    end_time = 0
    w_video, h_video = video_Clip.size

    # Loop through images and audios to create video clips
    for c, a in zip(images, audios):
        image_clip = configure_image(c, w_video, h_video)  # Assuming configure_image is defined elsewhere
        audio_clip = AudioFileClip(a).set_start(end_time)
        audio_clips.append(audio_clip)
        image_clips.append(
            image_clip.set_start(end_time)
                      .set_pos("center", "center")
                      .set_duration(audio_clip.duration)
                      .set_audio(audio_clip)
        )
        end_time += audio_clip.duration + 0.75  # Adjust end time with a small buffer

    # Ensure the background video is long enough
    if video_Clip.duration < end_time:
        video_Clip = video_Clip.fx(vfx.loop, duration=end_time + 0.75)
    else:
        video_Clip = video_Clip.subclip(0, end_time + 0.75)

    # Create the final audio from all audio clips
    audio_final = CompositeAudioClip(audio_clips)
    video_Clip.audio = audio_final

    # Create the final video file by combining the video and images
    final_video_file = CompositeVideoClip([video_Clip, *image_clips])

    # Add background music
    secs = final_video_file.duration
    bg_audio = get_bg('*.mp3')
    if not bg_audio:
        print("No background music file found.")
        return
    back_audio = AudioFileClip(bg_audio).volumex(0.3)

    # Loop the background audio if necessary
    if back_audio.duration < secs:
        back_audio = afx.audio_loop(back_audio, duration=secs)

    # Combine final video audio with background music
    final_audio = CompositeAudioClip([final_video_file.audio, back_audio])
    final_video_file = final_video_file.set_audio(final_audio)
    final_video_file = final_video_file.set_duration(secs)

    # Write the final video to a file
    final_video_file.write_videofile("./final_video.mp4", audio_codec='aac', fps=30, threads=4)

    

def configure_image(image,w_video,h_video):

    image_clip = ImageClip(image)
    margin = 20
    w_img , h_img = image_clip.size
    width_to_set = w_video - margin
    height_to_set = width_to_set * h_img / w_video

    image_clip = image_clip.resize(
        (width_to_set, height_to_set + 70),Image.Resampling.LANCZOS)
    
    return image_clip


def get_bg(ext):
    folder = ""
    
    if ext == "*.mp4":
        folder = os.path.join(".", "bg_video")
    else:
        folder = os.path.join(".", "bg_music")
    
    # Initialize result variable
    rslt = ""
    
    # Check if the folder exists and list its contents
    if os.path.exists(folder) and os.listdir(folder):
        for file in os.listdir(folder):
            if fnmatch.fnmatch(file, ext):  # Case-insensitive match
                print(file)
                rslt = os.path.join(folder, file)
                return rslt
    
    # Return an empty string if no match is found
    return rslt