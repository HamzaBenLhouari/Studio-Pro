"""
9-input_add_text_to_video
9-output_add_text_to_video
"""
import os
import fnmatch
from moviepy.editor import TextClip, VideoFileClip, CompositeVideoClip

def get_file(extensions):
    rslt=""
    # Folder containing images
    folder = "./9-input_add_text_to_video"
    listdir = os.listdir(folder)
    if len(listdir) == 0 :
        return ""
    for file in listdir:
        if fnmatch.fnmatch(file.lower(), extensions):
            print(file)
            rslt = os.path.join(folder, file)
            return rslt
    if rslt == "":
        return
    
def generate_video(text,video):

    clip = VideoFileClip(video)

    txt_clip = TextClip(text,font='DejaVu-Sans-Mono-Bold', fontsize = 75, color = 'black') 

    txt_clip = txt_clip.set_pos('center').set_duration(10)#.set_start(start_time)
    
    # Overlay the text clip on the first video clip 
    final_video = CompositeVideoClip([clip, txt_clip])

    final_video.write_videofile("./9-output_add_text_to_video/out.mp4",
                              audio_codec='aac', threads=6)

def get_content(file):
    script=""
    with open(file) as f:
        script = f.read()
    if script == "" :
        print("script is empty")
    else : print("text script done")
    return script

def main():
    video = get_file('*.mp4')
    text_file = get_file('*.txt')
    text = get_content(text_file)
    if (text == "" or video == "" ):
        return
    
    generate_video(text,video)

main()