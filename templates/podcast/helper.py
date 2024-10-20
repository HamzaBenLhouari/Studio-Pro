import os
import fnmatch
import os, requests, base64, playsound
from moviepy.editor import concatenate_audioclips, AudioFileClip, VideoFileClip, ImageClip, CompositeVideoClip, CompositeAudioClip
import re
import time
import moviepy.video.fx.all as vfx
import moviepy.audio.fx.all as afx
session_id="32d5799cd747a4e2ce47cafb59a1a0e4"

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
    print("getting text script")
    script=""
    with open("./script/script.txt") as f:
        script = f.read()
    if script == "" :
        print("script is empty")
    else : print("text script done")
    return script

def generate_voice():

    script = get_script()
    if script == "" :
        return
        
    script=re.sub(r'\n','',script)
    voices = script.split("##")
    i=1
    audios=[]
    for voice in voices:
        rep=voice.split(":")
        model=rep[0].replace(" ", "")
        voice_type=voice_character[model]
        if (voice_type and len(rep[1])<300 ):
            time.sleep(10)
            tts(session_id,voice_type,rep[1],"./audios/voice{}.mp3".format(i),False)
            time.sleep(10)
            audios.append("./audios/voice{}.mp3".format(i))
            #audios.append("./audios/silence.mp3")
            i=i+1
        else :
            print(f"error in voice type or length of text")
    audios.append("./audios/silence.mp3")
    clips = [AudioFileClip(c) for c in audios]
    final_clip = concatenate_audioclips(clips)
    final_clip = final_clip.volumex(1.7)
    final_clip.write_audiofile("./audios/voice.mp3")
    for audio in audios :
        if audio != "./audios/silence.mp3":
            os.remove(audio)

def generate_video():
    image = get_file("img")
    if image == "":
        print("no image found!")
        return
    
    audio= get_file("audio")
    if audio == "":
        print("no audio found!")
        return
    
    bg_music = get_file("bg_m")
    if bg_music == "":
        print("no background music found!")
        return

    audio = AudioFileClip(audio)
    image = ImageClip(image)
    bg_music= AudioFileClip(bg_music)

    if bg_music.duration < audio.duration:
        bg_music=afx.audio_loop(audio,duration=audio.duration+1)
        bg_music.fx(afx.audio_fadein,1).fx(afx.audio_fadeout,1)
    else :
        bg_music = bg_music.subclip(0, audio.duration+5)
        bg_music.fx(afx.audio_fadein,1).fx(afx.audio_fadeout,1)

    final_audio = CompositeAudioClip([bg_music,audio])
    final_clip = image.set_duration(final_audio.duration).set_audio(final_audio)
    final_clip = final_clip.fx(vfx.fadein,1).fx(vfx.fadeout,1)
    final_clip.write_videofile("./finalvideo.mp4",
                              audio_codec='aac', fps=30, threads=4)

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
    folder=""
    if file == "img":
        image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.tiff']
        folder = "./image"
        listdir = os.listdir(folder)
        for file in listdir:
            if any(fnmatch.fnmatch(file.lower(), ext) for ext in image_extensions):
                rslt = os.path.join(folder, file)
                return rslt
    if file == "audio":
        folder = "./audios"
        listdir = os.listdir(folder)
        for file in listdir:
            if fnmatch.fnmatch(file.lower(), 'voice.mp3'):
                rslt = os.path.join(folder, file)
                return rslt
    if file == "bg_m":
        folder = "./bg_music"
        listdir = os.listdir(folder)
        for file in listdir:
            if fnmatch.fnmatch(file.lower(), '*.mp3'):
                rslt = os.path.join(folder, file)
                return rslt
    return rslt