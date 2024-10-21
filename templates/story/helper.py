import os
import time
import re
import fnmatch
from elevenlabs import set_api_key,generate, play, save, voices, Voice, VoiceSettings
from moviepy.editor import concatenate_audioclips, CompositeAudioClip, CompositeVideoClip, AudioFileClip, ImageClip
import moviepy.video.fx.all as vfx
import moviepy.audio.fx.all as afx

ELEVENLAB_KEY="3cd04161eb64b39de66b5d198babc762"

voice_character = {
    "Narrator":"Bill",
    "Narrator_2":"Lily",
    "Narrator_3":"Matilda",
    "Narrator_4":"Sarah",
    "Narrator_5":"Will",
    }


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

    api_key=ELEVENLAB_KEY

    if api_key == "":
        return

    set_api_key(api_key)

    my_text=get_script()

    if my_text == "":
        return
    
    my_text=re.sub(r'\n','',my_text)
    results = my_text.split("##")

    i=1
    for result in results :
        if "$$" in result:
            audios=[]
            j=1
            frames = result.split("$$")
            for frame in frames:
                voice_and_character = frame.split(":")
                model=voice_and_character[0].replace(" ", "")
                model=voice_character[model]
                if model : 
                    audio = generate(
                        text=voice_and_character[1],
                        voice=model,
                        model="eleven_multilingual_v2"
                    )
                    time.sleep(5)
                    file = "./voice{}.mp3".format(j)
                    save(audio,file)
                    audios.append(file)
                    audios.append("./silence.mp3")
                    j=j+1
                else :
                     print(f"something wrong with voice model {i}")
                     print(f"something wrong with voice model frame {j}")
            clips = [AudioFileClip(c) for c in audios]
            final_clip = concatenate_audioclips(clips)
            final_clip = final_clip.volumex(1.7)
            final_clip.write_audiofile("./audios/frame{}.mp3".format(i))

            for audio in audios :
                if audio != "./silence.mp3":
                    os.remove(audio)

        else:
            voice_and_character = result.split(":")
            model=voice_and_character[0].replace(" ", "")
            model=voice_character[model]
            if model : 
                audio = generate(
                    text=voice_and_character[1],
                    voice=model,
                    model="eleven_multilingual_v2"
                )
                time.sleep(5)
                file = "./audios/frame{}.mp3".format(i)
                save(audio,file)
            else :
                print(f"something wrong with voice model {i}")
        
        i=i+1
    

def generate_video():
    images = fetch_images()
    audios = fetch_audios()
    image_clips=[]
    if (len(images)==0 or len(audios)==0)or(len(images)!=len(audios)):
        print("verify your files please!")
        return
    end_time=0
    for (image, audio) in zip(images, audios):
        audioClip = AudioFileClip(audio).fx(afx.audio_fadein,1).fx(afx.audio_fadeout,1).set_start(end_time)
        imageClip = ImageClip(image).set_duration(audioClip.duration).set_audio(audioClip).set_start(end_time)
        image_clips.append(imageClip.fx(vfx.fadein,1).fx(vfx.fadeout,1))
        end_time=end_time+audioClip.duration+1
    final_video_file = CompositeVideoClip([*image_clips])

    # adding background music 

    secs=final_video_file.duration
    bg_audio = get_bg()
    back_audio = AudioFileClip(bg_audio).volumex(0.3)
    
    if back_audio.duration < end_time :
        back_audio=afx.audio_loop(back_audio,duration=end_time)
        back_audio.fx(afx.audio_fadein,1).fx(afx.audio_fadeout,1)
    else :
        back_audio = back_audio.subclip(0, end_time)
        back_audio.fx(afx.audio_fadein,1).fx(afx.audio_fadeout,1)
      
    final_audio = CompositeAudioClip([final_video_file.audio,back_audio])
    final_video_file = final_video_file.set_audio(final_audio)
    final_video_file = final_video_file.set_duration(secs)
        
    final_video_file.write_videofile("./finalvideo.mp4",
                              audio_codec='aac', fps=30, threads=4)


def fetch_audios():
    print("getting audios")
    audios=[]
    files = os.listdir('./audios')
    sorted_files = sorted(files)
    for file in sorted_files:
        if fnmatch.fnmatch(file, '*.mp3'):
            print(file)
            audios.append("./audios/"+file)
    if len(audios) == 0:
        print("audios not found")
    print("audios done")
    return audios


def fetch_images():
    print("getting images")
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.tiff']
    images=[]
    files = os.listdir('./images')
    sorted_files = sorted(files)
    for file in sorted_files:
        if any(fnmatch.fnmatch(file.lower(), ext) for ext in image_extensions):
            print(file)
            images.append("./images/"+file)
    if len(images) == 0:
        print("images not found")
    print("images done")
    return images


def get_bg():
    folder = "./bg_music"
    rslt=""
    listdir = os.listdir(folder)
    if len(listdir) != 0 :
        for file in listdir:
            if fnmatch.fnmatch(file.lower(), '*.mp3'):
                print(file)
                rslt = os.path.join(folder, file)
                return rslt
    return rslt