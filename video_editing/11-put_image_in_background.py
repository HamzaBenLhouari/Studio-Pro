"""
11-input_image_in_background
bg_img
11-output_image_in_background
"""
import os
import fnmatch
from moviepy.editor import ImageClip, VideoFileClip, CompositeVideoClip

def get_files(tmp):
    dir = ""
    extensions=[]
    if tmp == "videos":
        dir="./11-input_image_in_background"
        extensions=["*.mp4"]
    if tmp == "bg_img":
        dir = "./11-input_image_in_background/bg_img"
        extensions=['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.tiff']
    print("getting videos")
    files=[]
    for file in os.listdir(dir):
        if any(fnmatch.fnmatch(file.lower(), ext) for ext in extensions):
            print(file)
            files.append(os.path.join(dir, file))
            if tmp == "bg_img":
                return files
    if len(files) == 0:
        return files
    print("files done")
    return files

def put_bg_img(videos,bg_img):

    img_clip=ImageClip(bg_img[0])

    w_video, h_video = img_clip.size
    width_to_set = w_video*0.8
    height_to_set = h_video*0.8

    video_clips = []
    end_time=2

    for video in videos:
        clip = VideoFileClip(video)#.resize((width_to_set,height_to_set))
        clip= clip.set_pos(("center", "center")).set_start(end_time).crossfadein(1)
        video_clips.append(clip)
        end_time=end_time+clip.duration+1

    img_clip = img_clip.set_duration(end_time)

    final_video_file = CompositeVideoClip([img_clip, *video_clips])
        
    final_video_file.write_videofile("./11-output_image_in_background/out.mp4",
                                    remove_temp=True,
                                    codec="libx264",
                                    audio_codec="aac",
                                    threads = 6)
    
def main():
    videos = get_files("videos")
    bg_img = get_files("bg_img")
    if(len(videos)==0 or len(bg_img)==0):
        print("check your files")
        return
    put_bg_img(videos,bg_img)

main()