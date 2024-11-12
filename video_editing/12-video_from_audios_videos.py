"""
12-input_video_from_audios_videos
videos
audios
12-output_video_from_audios_videos
"""
from moviepy.editor import AudioFileClip, VideoFileClip, concatenate_videoclips
import moviepy.video.fx.all as vfx
import moviepy.audio.fx.all as afx
import os
import fnmatch

def fetch_audios():
    print("getting audios")
    folder="./12-input_video_from_audios_videos/audios"
    audios=[]
    for file in os.listdir(folder):
        if fnmatch.fnmatch(file, '*.mp3'):
            print(file)
            audios.append(os.path.join(folder, file))
    if len(audios) == 0:
        return audios
    print("audios done")
    return audios

def fetch_videos():
    print("getting videos")
    folder="./12-input_video_from_audios_videos/videos"
    videos=[]
    for file in os.listdir(folder):
        if fnmatch.fnmatch(file, '*.mp4'):
            print(file)
            videos.append(os.path.join(folder, file))
    if len(videos) == 0:
        print("videos not found")
    print("videos done")
    return videos
def create_video(videos,audios):
    videoclips = []
    videoclipsList = []
    addressvideo=""
    i=1
    for (video, audio) in zip(videos, audios):
        audioClip = AudioFileClip(audio).fx(afx.audio_fadein,1).fx(afx.audio_fadeout,1)
        videoClip = VideoFileClip(video)
        if videoClip.duration < audioClip.duration :
            videoClip=videoClip.fx(vfx.loop,duration=audioClip.duration+0.75)
            
        videoClip = videoClip.set_duration(audioClip.duration)
        videoClip = videoClip.set_audio(audioClip)
        #addressvideo="./12-output_video_from_audios_videos/out{}.mp4".format(i)
        """videoClip.write_videofile(addressvideo,fps=30,remove_temp=True,
                                        codec="libx264",
                                        audio_codec="aac",
                                        threads = 6)"""
        i=i+1
        #videoclips.append(addressvideo)
        videoclipsList.append(videoClip)
    
    for i in range(len(videoclipsList)):
        videoclipsList[i] = videoclipsList[i].fx(vfx.fadeout,1)
    video2=concatenate_videoclips(videoclipsList)
    video2.write_videofile("./12-output_video_from_audios_videos/out.mp4", fps=30,remove_temp=True,
                                        codec="libx264",
                                        audio_codec="aac",
                                        threads = 6)
    """for video in videoclips :
        os.remove(video)"""
def main():
    videos = fetch_videos()
    audios = fetch_audios()
    if (len(videos)==0 or len(audios)==0)or(len(videos)!=len(audios)):
        print("verify your files please!")
        return
    create_video(videos,audios)
main()
