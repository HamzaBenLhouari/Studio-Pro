"""
don t forget to separate each paragraph with "##" in the script.txt
the max length of a paragraph should be lower than 300 character
"""
from helper_conf_tiktok import get_script, get_sessionid, get_voice_type, tts
from moviepy.editor import concatenate_audioclips, AudioFileClip
import time
def generate_final_voice(sessionid,voice_type,script):
    voices = script.split("##")
    i=1
    audios=[]
    for voice in voices:
        tts(sessionid,voice_type,voice,"./output_tiktok_tts/voice{}.mp3".format(i),False)
        time.sleep(5)
        audios.append("./output_tiktok_tts/voice{}.mp3".format(i))
        i=i+1
    clips = [AudioFileClip(c) for c in audios]
    final_clip = concatenate_audioclips(clips)
    final_clip.write_audiofile("./output_tiktok_tts/voice.mp3")
    print(audios)

def main():
    
    script = get_script()
    if script == "" :
        return

    sessionid = get_sessionid()
    if sessionid == "" :
        return
        
    voice_type = get_voice_type()
    if voice_type == "":
        return
    
    generate_final_voice(sessionid,voice_type,script)

main()