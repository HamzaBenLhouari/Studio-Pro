"""
    You Need Input Files Here (Audios)
    Put your Audios in "7-input_concatenate_audios" directory 
    and wait the output audios in 
    "7-output_concatenate_audios" directory
    You can set volume value for the final audio
        search volumex() 
"""
import os
import fnmatch
from moviepy.editor import AudioFileClip, concatenate_audioclips

def fetch_audios():
    print("getting audios")
    audios=[]
    for file in os.listdir('./7-input_concatenate_audios'):
        if fnmatch.fnmatch(file, '*.mp3'):
            print(file)
            audios.append("./7-input_concatenate_audios/"+file)
    if len(audios) == 0:
        return audios
    print("audios done")
    return audios

def concatenate_audios(audios):
    audios = [AudioFileClip(i).volumex(1.7) for i in audios]
    audio = concatenate_audioclips(audios)
    audio.write_audiofile("./7-output_concatenate_audios/out.mp3")

def main():

    audios = fetch_audios()

    if len(audios) <= 1 :
        print("PLease Verify! You must have more than one audio")
        return
    
    concatenate_audios(audios)

main()