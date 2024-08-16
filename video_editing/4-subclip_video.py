"""
    This Script takes the first Video in tha path given
    You Need Input Video File Here
    Put your Video in "4-input_video" directory 
    and wait the output video in 
    "4-output_subclip" directory
    ++++++++++++++++++++++++++++
    We can use One of Two Methods to subclip a Video
"""
import os
import fnmatch
from moviepy.editor import VideoFileClip


def video_to_subclip():
    print("getting video")

    listdir = os.listdir('./4-input_video')
    if len(listdir) == 0 :
        print("video not found")
        return ""
    
    video=listdir[0]
    
    if fnmatch.fnmatch(video, '*.mp4'):
        print(video)
        video="./4-input_video/"+video
        print("videos done")
        return video
    else :
        return ""
    
def subclip_video(video):
    #Starting time
    start_h=0
    start_min=0
    start_sec=3

    start_time = (start_h*3600) + (start_min*60) + (start_sec)
    # You can use this format also
    #start_time="01:03:05.35"
    #ending time
    end_h=0
    end_min=0
    end_sec=6
    end_time = (end_h*3600) + (end_min*60) + (end_sec)
    # You can use this format also
    #end_time="01:03:05.35"

    video_clip = VideoFileClip(video)

    if start_time < end_time :

        final_video_file = video_clip.subclip(start_time, end_time)
        
        final_video_file.write_videofile("./4-output_subclip/out.mp4",
                                    fps=30,
                                    remove_temp=True,
                                    codec="libx264",
                                    audio_codec="aac",
                                    threads = 6)
    else : 
        print("check time")

def main():
    video = video_to_subclip()
    if video == "" :
        print("video not found")
        return
    subclip_video(video)

main()