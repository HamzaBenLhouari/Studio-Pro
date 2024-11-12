"""
    This Script takes the first Video in tha path given
    You Need Input Video File Here
    Put your Video in "5-input_video_to_audio" directory 
    and wait the output audio in 
    "5-output_audio" directory
"""
import os
import fnmatch
from moviepy.editor import VideoFileClip


def get_video():
    print("getting video")

    listdir = os.listdir('./5-input_video_to_audio')
    if len(listdir) == 0 :
        print("video not found")
        return ""
    
    video=listdir[0]
    
    if fnmatch.fnmatch(video, '*.mp4'):
        print(video)
        video="./5-input_video_to_audio/"+video
        print("videos done")
        return video
    else :
        return ""
    
def get_audio(video):

    video = VideoFileClip(video)
    audio = video.audio
    audio.write_audiofile("./5-output_audio/out.mp3")

def main():

    video = get_video()
    if video == "" :
        print("video not found")
        return
    get_audio(video)

main()