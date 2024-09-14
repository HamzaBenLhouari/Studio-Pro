from elevenlabs import set_api_key,generate, save
from helper_config import get_api_key, get_text, get_voice_model
from moviepy.editor import concatenate_audioclips, AudioFileClip
import time

def main():

    api_key=get_api_key()

    if api_key == "":
        return

    set_api_key(api_key)

    my_text=get_text()

    if my_text == "":
        return

    voice_model=get_voice_model()

    if voice_model == "":
        return

    results = my_text.split("##")

    i=1

    audios=[]
      

    for result in results :
        """
        # just for english content
        audio = generate(
            text=my_text,
            voice=Voice(
                voice_id='piTKgcLEGmPE4e6mEKli',
                settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True)
            )
        )"""
        
        # for all languages 
        audio = generate(
        text=result,
        voice=voice_model,
        model="eleven_multilingual_v2"
        )

        time.sleep(10)
        file = "./output_eleven_labs_tts/voice{}.mp3".format(i)
        save(audio,file)
        time.sleep(5)
        audios.append(file)
        #audios.append("./output_eleven_labs_tts/silence.mp3")
        i=i+1
    clips = [AudioFileClip(c) for c in audios]
    final_clip = concatenate_audioclips(clips)
    final_clip = final_clip.volumex(1.7)
    final_clip.write_audiofile("./output_eleven_labs_tts/voice.mp3")

    

main()