import os
import time
import re
import fnmatch
from dotenv import load_dotenv
from elevenlabs import set_api_key,generate, save
from moviepy.editor import concatenate_audioclips, CompositeAudioClip, CompositeVideoClip, AudioFileClip, ImageClip
import moviepy.video.fx.all as vfx
import moviepy.audio.fx.all as afx

# Load environment variables from the .env file
load_dotenv()

# Assuming voice_character is a predefined dictionary that maps voice names to voice models
voice_character = {
    "Narrator":"Bill",
    "Narrator_2":"Lily",
    "Narrator_3":"Matilda",
    "Narrator_4":"Sarah",
    "Narrator_5":"Will",
    }


def get_script():
    """
    Reads the text script from the file located at './script/script.txt'.
    Returns the content of the script as a string. If the script is empty, it logs a message.
    """
    script_path = "./script/script.txt"

    if not os.path.exists(script_path):
        print(f"Error: The script file at '{script_path}' does not exist.")
        return ""
    
    print("Getting text script...")
    with open(script_path, 'r') as f:
        script = f.read()

    if not script:
        print("Warning: The script is empty.")
    else:
        print("Text script loaded successfully.")

    return script

def generate_voice():
    # Retrieve the Eleven Labs API key from the environment variables
    api_key = os.getenv('ELEVEN_LABS_KEY')

    if not api_key:
        print("Error: ELEVEN_LABS_KEY not found in .env file.")
        return

    # Set the API key for Eleven Labs
    set_api_key(api_key)

    # Get the text script to generate audio from
    my_text = get_script()

    if not my_text:
        print("Error: The script is empty.")
        return

    # Clean up text by removing newlines and splitting by paragraphs
    my_text = re.sub(r'\n', '', my_text)
    results = my_text.split("##")

    # Process each paragraph or frame
    for i, result in enumerate(results, 1):
        audios = []

        if "$$" in result:
            # Handle multi-frame paragraphs (split by $$)
            frames = result.split("$$")
            for j, frame in enumerate(frames, 1):
                voice_and_character = frame.split(":")
                model_name = voice_and_character[0].strip()
                model = voice_character.get(model_name)

                if model:
                    audio = generate(
                        text=voice_and_character[1],
                        voice=model,
                        model="eleven_multilingual_v2"
                    )
                    time.sleep(5)  # Adjust sleep time if necessary
                    file = f"./audios/frame{i}_audio{j}.mp3"
                    save(audio, file)
                    audios.append(file)
                    audios.append("./silence.mp3")  # Add silence between frames
                else:
                    print(f"Error: Invalid voice model in frame {i}, subframe {j}")
            
            # Concatenate audio clips for this frame
            clips = [AudioFileClip(c) for c in audios if c != "./silence.mp3"]
            final_clip = concatenate_audioclips(clips)
            final_clip = final_clip.volumex(1.7)
            final_clip.write_audiofile(f"./audios/frame{i}.mp3")
            
            # Clean up individual audio files
            for audio in audios:
                if audio != "./silence.mp3":
                    os.remove(audio)

        else:
            # Handle single-frame paragraphs (no $$ separator)
            voice_and_character = result.split(":")
            model_name = voice_and_character[0].strip()
            model = voice_character.get(model_name)

            if model:
                audio = generate(
                    text=voice_and_character[1],
                    voice=model,
                    model="eleven_multilingual_v2"
                )
                time.sleep(5)  # Adjust sleep time if necessary
                file = f"./audios/frame{i}.mp3"
                save(audio, file)
            else:
                print(f"Error: Invalid voice model in frame {i}")


def generate_video():
    """
    Generates a video from images and audios, combining them with a background music track.
    The audio and image clips are synchronized, and video transitions like fade-in and fade-out are applied.
    """
    images = fetch_images()
    audios = fetch_audios()

    if len(images) == 0 or len(audios) == 0 or len(images) != len(audios):
        print("Verification failed: Ensure you have equal numbers of images and audios, and that both folders contain files.")
        return
    
    image_clips = []
    end_time = 0

    # Create video clips from image and audio pairs
    for image, audio in zip(images, audios):
        # Apply fade effects to audio
        audio_clip = AudioFileClip(audio).fx(afx.audio_fadein, 1).fx(afx.audio_fadeout, 1).set_start(end_time)
        
        # Create image clip and sync with audio
        image_clip = ImageClip(image).set_duration(audio_clip.duration).set_audio(audio_clip).set_start(end_time)
        
        # Apply fade effects to the image
        image_clips.append(image_clip.fx(vfx.fadein, 1).fx(vfx.fadeout, 1))
        
        end_time += audio_clip.duration + 1  # Add duration plus 1 second for spacing

    # Combine all image clips into one video
    final_video = CompositeVideoClip(image_clips)

    # Adding background music
    bg_audio = get_bg()
    back_audio = AudioFileClip(bg_audio).volumex(0.3)

    # Adjust background music length to match video length
    if back_audio.duration < final_video.duration:
        back_audio = afx.audio_loop(back_audio, duration=final_video.duration)
    else:
        back_audio = back_audio.subclip(0, final_video.duration)

    # Apply fade effects to the background audio
    back_audio = back_audio.fx(afx.audio_fadein, 1).fx(afx.audio_fadeout, 1)

    # Combine final audio (video audio + background music)
    final_audio = CompositeAudioClip([final_video.audio, back_audio])

    # Set final audio and duration to the video
    final_video = final_video.set_audio(final_audio).set_duration(final_video.duration)

    # Write the final video to a file
    final_video.write_videofile("./finalvideo.mp4", audio_codec='aac', fps=30, threads=4)


def fetch_audios():
    """
    Fetches and returns a sorted list of audio file paths from the 'audios' folder.
    Only .mp3 files are considered.
    """
    print("Getting audios...")
    folder = './audios'
    
    # Collect all .mp3 files
    audios = [
        os.path.join(folder, file) 
        for file in sorted(os.listdir(folder))
        if fnmatch.fnmatch(file.lower(), '*.mp3')
    ]

    if audios:
        print("Audios found:", audios)
    else:
        print("No audios found")
    
    return audios


def fetch_images():
    """
    Fetches and returns a sorted list of image file paths from the 'images' folder.
    Supports common image formats (jpg, jpeg, png, bmp, gif, tiff).
    """
    print("Getting images...")
    image_extensions = ('*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.tiff')
    folder = './images'
    
    # Collect all images with matching extensions
    images = [
        os.path.join(folder, file) 
        for file in sorted(os.listdir(folder))
        if any(fnmatch.fnmatch(file.lower(), ext) for ext in image_extensions)
    ]

    if images:
        print("Images found:", images)
    else:
        print("No images found")
    
    return images

def get_bg():
    """
    Finds and returns the path of the first .mp3 file in the bg_music folder.
    If no .mp3 files are found, returns an empty string.
    """
    folder = "./bg_music"
    for file in os.listdir(folder):
        if fnmatch.fnmatch(file.lower(), '*.mp3'):
            print(f"Background music file found: {file}")
            return os.path.join(folder, file)
    
    print("No background music file found")
    return ""
