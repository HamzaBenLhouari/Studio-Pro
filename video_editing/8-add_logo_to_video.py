"""
8-input-add_logo_to_video
8-output-add_logo_to_video
"""
import os
import fnmatch
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip


def get_file(extensions):
    print("getting videos")
    rslt=""
    # Folder containing images
    folder = "./8-input-add_logo_to_video"
    listdir = os.listdir(folder)
    if len(listdir) == 0 :
        print("logo not found")
        return ""
    for file in listdir:
        if any(fnmatch.fnmatch(file.lower(), ext) for ext in extensions):
            print(file)
            rslt = os.path.join(folder, file)
            print("logo done")
            return rslt
    if rslt == "":
        return
    
def add_logo_to_video(logo,video):

    clip = VideoFileClip(video)

    logo = (ImageClip(logo)
            .set_duration(clip.duration)
            #.resize(height=50) # if you need to resize...
            .margin(right=8, top=8, opacity=0) # (optional) logo-border padding
            .set_pos(("right","top")))

    final = CompositeVideoClip([clip, logo])
    final.write_videofile("./8-output-add_logo_to_video/out.mp4",fps=30,remove_temp=True,
                                        codec="libx264",
                                        audio_codec="aac",
                                        threads = 6)

def main():
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.tiff']
    logo=get_file(image_extensions)
    video = get_file(['*.mp4'])
    if (logo == "" or video == "" ):
        return
    add_logo_to_video(logo,video)
main()