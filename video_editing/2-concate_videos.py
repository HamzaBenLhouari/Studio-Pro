"""
    You Need Input Files Here (Videos)
    Put your Videos in "2-input_concate_videos" directory 
    and wait the output video in 
    "2-output_concate_videos" directory
"""
import os
import fnmatch
from moviepy.editor import concatenate_videoclips, VideoFileClip

def fetch_videos():
    print("getting videos")
    videos=[]
    for file in os.listdir('./2-input_concate_videos'):
        if fnmatch.fnmatch(file, '*.mp4'):
            print(file)
            videos.append("./2-input_concate_videos/"+file)
    if len(videos) == 0:
        print("videos not found")
        return videos
    print("videos done")
    return videos

def create_video_from_videos(videos):
    video = [VideoFileClip(i) for i in videos]
    video = concatenate_videoclips(video,method='compose')
    video.write_videofile("./2-output_concate_videos/out.mp4", fps=30,remove_temp=True,
                                        codec="libx264",
                                        audio_codec="aac",
                                        threads = 6)

    
def main():
    videos = fetch_videos()
    if len(videos) <= 1 :
        print("PLease Verify! You must have more than one Video")
        return
    create_video_from_videos(videos)
    
main()