import os
import fnmatch
import os, requests, base64, playsound
from moviepy.editor import concatenate_audioclips, AudioFileClip, VideoFileClip, ImageClip, CompositeVideoClip, CompositeAudioClip
import re
import time
import moviepy.video.fx.all as vfx
import moviepy.audio.fx.all as afx
from dotenv import load_dotenv
# Ensure environment variables are loaded
load_dotenv()

voice_character={
    "podcaster":"en_us_002",
    "guest_1":"en_us_006",
    "guest_2":"en_au_001",
    "guest_3":"en_us_001",
    "guest_4":"en_female_emotional",
}
"""
    'en_au_001',                  # English AU - Female
    'en_au_002',                  # English AU - Male
    'en_uk_001',                  # English UK - Male 1
    'en_uk_003',                  # English UK - Male 2
    'en_us_001',                  # English US - Female (Int. 1)
    'en_us_002',                  # English US - Female (Int. 2)
    'en_us_006',                  # English US - Male 1
    'en_us_007',                  # English US - Male 2
    'en_us_009',                  # English US - Male 3
    'en_us_010',                  # English US - Male 4 

    # OTHER
    'en_male_narration'           # narrator
    'en_male_funny'               # wacky
    'en_female_emotional'         # peaceful
    
    # DISNEY VOICES
    'en_us_ghostface',            # Ghost Face
    'en_us_c3po',                 # C3PO
    'en_us_stitch',               # Stitch
    'en_us_stormtrooper',         # Stormtrooper
    'en_us_rocket',               # Rocket
"""

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

    # Retrieve session_id from the .env file
    session_id = os.getenv('TIKTOK_SESSION_ID')

    if not session_id:
        print("Error: TIKTOK_SESSION_ID not found in .env file.")
        return
    
    # Get the script content
    script = get_script()
    if script == "":
        return
        
    script = re.sub(r'\n', '', script)
    voices = script.split("##")
    i = 1
    audios = []

    # Loop through each voice section in the script
    for voice in voices:
        rep = voice.split(":")
        model = rep[0].replace(" ", "")
        voice_type = voice_character[model]  # Assuming voice_character is predefined
        if voice_type and len(rep[1]) < 300:
            time.sleep(10)
            # Call the tts function to generate voice
            tts(session_id, voice_type, rep[1], f"./audios/voice{i}.mp3", False)
            time.sleep(10)
            audios.append(f"./audios/voice{i}.mp3")
            i += 1
        else:
            print(f"Error in voice type or length of text")

    audios.append("./audios/silence.mp3")  # Adding silence to the end for proper audio flow

    # Combine all audio clips
    clips = [AudioFileClip(c) for c in audios]
    final_clip = concatenate_audioclips(clips)
    final_clip = final_clip.volumex(1.7)  # Adjust volume
    final_clip.write_audiofile("./audios/voice.mp3")  # Save the final audio

    # Clean up temporary audio files
    for audio in audios:
        if audio != "./audios/silence.mp3":
            os.remove(audio)

def generate_video():
    # Retrieve file paths for image, audio, and background music
    image = get_file("img")
    if not image:
        print("No image found!")
        return
    
    audio = get_file("audio")
    if not audio:
        print("No audio found!")
        return
    
    bg_music = get_file("bg_m")
    if not bg_music:
        print("No background music found!")
        return

    # Load the image, audio, and background music clips
    image_clip = ImageClip(image)
    audio_clip = AudioFileClip(audio)
    bg_music_clip = AudioFileClip(bg_music).volumex(0.3)

    # Adjust background music duration
    if bg_music_clip.duration < audio_clip.duration:
        bg_music_clip = afx.audio_loop(bg_music_clip, duration=audio_clip.duration + 1)
    else:
        bg_music_clip = bg_music_clip.subclip(0, audio_clip.duration + 1)
    
    # Apply fade effects to background music and final video clip
    bg_music_clip = bg_music_clip.fx(afx.audio_fadein, 1).fx(afx.audio_fadeout, 1)
    
    # Combine background music and audio
    final_audio = CompositeAudioClip([bg_music_clip, audio_clip])
    
    # Set the duration of the image clip to match the final audio
    final_clip = image_clip.set_duration(final_audio.duration).set_audio(final_audio)
    
    # Apply fade-in and fade-out effects to the video
    final_clip = final_clip.fx(vfx.fadein, 1).fx(vfx.fadeout, 1)
    
    # Write the final video to a file
    final_clip.write_videofile("./finalvideo.mp4", audio_codec='aac', fps=30, threads=4)

def tts(session_id: str, text_speaker: str = "en_us_002", req_text: str = "TikTok Text To Speech", filename: str = 'voice.mp3', play: bool = False):

    req_text = req_text.replace("+", "plus")
    req_text = req_text.replace(" ", "+")
    req_text = req_text.replace("&", "and")

    headers = {
        'User-Agent': 'com.zhiliaoapp.musically/2022600030 (Linux; U; Android 7.1.2; es_ES; SM-G988N; Build/NRD90M;tt-ok/3.12.13.1)',
        'Cookie': f'sessionid={session_id}'
    }
    url = f"https://api22-normal-c-useast1a.tiktokv.com/media/api/text/speech/invoke/?text_speaker={text_speaker}&req_text={req_text}&speaker_map_type=0&aid=1233"
    r = requests.post(url, headers = headers)

    if r.json()["message"] == "Couldn't load speech. Try again.":
        output_data = {"status": "Session ID is invalid", "status_code": 5}
        print(output_data)
        return output_data

    vstr = [r.json()["data"]["v_str"]][0]
    msg = [r.json()["message"]][0]
    scode = [r.json()["status_code"]][0]
    log = [r.json()["extra"]["log_id"]][0]
    
    dur = [r.json()["data"]["duration"]][0]
    spkr = [r.json()["data"]["speaker"]][0]

    b64d = base64.b64decode(vstr)

    with open(filename, "wb") as out:
        out.write(b64d)

    output_data = {
        "status": msg.capitalize(),
        "status_code": scode,
        "duration": dur,
        "speaker": spkr,
        "log": log
    }

    print(output_data)

    if play is True:
        playsound.playsound(filename)
        os.remove(filename)

    return output_data

def get_file(file):
    rslt = ""
    folder = ""
    # List of image extensions to check
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.tiff']

    # Check for 'img' files (image files)
    if file == "img":
        folder = "./image"  # Assuming image folder is './image'
        listdir = os.listdir(folder)
        for f in listdir:
            if any(fnmatch.fnmatch(f.lower(), ext) for ext in image_extensions):
                rslt = os.path.join(folder, f)
                return rslt  # Return first valid image found
    # Check for 'audio' files (audio files)
    elif file == "audio":
        folder = "./audios/"  # Assuming audio folder is './audios'
        listdir = os.listdir(folder)
        for f in listdir:
            if fnmatch.fnmatch(f.lower(), 'voice.mp3'):  # Assuming only 'voice.mp3' is expected
                rslt = os.path.join(folder, f)
                return rslt  # Return the first valid audio file found
    # Check for 'bg_m' files (background music files)
    elif file == "bg_m":
        folder = "./bg_music"  # Assuming background music folder is './bg_music'
        listdir = os.listdir(folder)
        for f in listdir:
            if fnmatch.fnmatch(f.lower(), '*.mp3'):  # Background music is expected to be an mp3 file
                rslt = os.path.join(folder, f)
                return rslt  # Return the first valid background music file found

    return rslt  # Return empty string if no valid file is found