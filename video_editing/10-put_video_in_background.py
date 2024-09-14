"""
10-input_video_in_background
bg_video
10-output_video_in_background
"""
import os
import fnmatch
from moviepy.editor import VideoFileClip, CompositeVideoClip
import moviepy.video.fx.all as vfx

def fetch_videos(tmp):
    dir = ""
    if tmp == "videos":
        dir="./10-input_video_in_background"
    if tmp == "bg_v":
        dir = "./10-input_video_in_background/bg_video"
    print("getting videos")
    videos=[]
    for file in os.listdir(dir):
        if fnmatch.fnmatch(file, '*.mp4'):
            print(file)
            videos.append(os.path.join(dir, file))
            if tmp == "bg_v":
                return videos
    if len(videos) == 0:
        return videos
    print("videos done")
    return videos

def put_bg_video(videos,bg_video):

    bg_v = VideoFileClip(bg_video[0])
    w_video, h_video = bg_v.size
    width_to_set = w_video*0.8
    height_to_set = h_video*0.8

    video_clips = []
    end_time=2

    for video in videos:
        clip = VideoFileClip(video)#.resize((width_to_set,height_to_set))
        clip= clip.set_pos(("center", "center")).set_start(end_time).crossfadein(1)
        video_clips.append(clip)
        end_time=end_time+clip.duration+1
    
    if bg_v.duration < end_time:
        bg_v = bg_v.fx(vfx.loop,duration=end_time)
    else : 
        bg_v.subclip(0,end_time)

    
    final_video_file = CompositeVideoClip([bg_v, *video_clips])
        
    final_video_file.write_videofile("./10-output_video_in_background/out.mp4",
                                    remove_temp=True,
                                    codec="libx264",
                                    audio_codec="aac",
                                    threads = 6)
def main():
    videos = fetch_videos("videos")
    bg_video = fetch_videos("bg_v")
    if(len(videos)==0 or len(bg_video)==0):
        print("check your videos")
        return
    put_bg_video(videos,bg_video)

main()