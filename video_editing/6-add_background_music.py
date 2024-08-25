"""
    This Script takes two first input files 
    ( video and background music)
    Put your video and background music
    in "6-input_video_bg_m" directory 
    and wait the output video in 
    "6-output_video_bg_m" directory
"""
import os
import fnmatch
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
import moviepy.audio.fx.all as afx

def get_file(ext):
    listdir = os.listdir('./6-input_video_bg_m')
    if len(listdir) == 0 :
        print("empty directory!")
        return "error"
    for file in listdir:
        if fnmatch.fnmatch(file.lower(), ext):
            print(file)
            file="./6-input_video_bg_m/"+file
            print("done")
            return file
    return ""

def add_bg_m_to_video(video,bg_m):

    # Load the video clip
    video = VideoFileClip(video)
    secs=video.duration
    audio_video=video.audio
    # Load the background music 
    
    try:
        audio = AudioFileClip(bg_m)
    except Exception as e:
        raise ValueError("Failed to load background music. Error: " + str(e))
    
    if audio is None:
        raise ValueError("The 'audio' clip failed to load and is None.")
    
    if audio_video is None:
        raise ValueError("The 'audio'video clip failed to load and is None.")
    
    # if you want to start the audio in a time prefered
    """t_start = "00:01:50.35"
    t_end = None
    audio = audio.subclip(t_start,t_end)"""
    if audio.duration < secs :
            audio=afx.audio_loop(audio,duration=secs)
    
    try:
        final_audio = CompositeAudioClip([audio_video, audio])
    except AttributeError as e:
        raise ValueError("Failed to combine audio clips. Error: " + str(e))

    # Set the composite audio track to the video
    video = video.set_audio(final_audio)
    video = video.set_duration(secs)
    video.write_videofile("./6-output_video_bg_m/out.mp4", fps=30,remove_temp=True,
                                    codec="libx264",
                                    audio_codec="aac",
                                    threads = 6)
    


def main():

    print("getting video")
    my_video = get_file("*.mp4")
    if my_video == "error" :
        return
    
    print("getting background music")

    my_bg_m = get_file("*.mp3")

    if (my_video == "" or my_bg_m == "" ):
        return
    
    add_bg_m_to_video(my_video,my_bg_m)

main()