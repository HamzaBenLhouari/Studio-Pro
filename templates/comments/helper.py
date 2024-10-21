from moviepy.editor import AudioFileClip, VideoFileClip, ImageClip, CompositeVideoClip, CompositeAudioClip
import moviepy.video.fx.all as vfx
import moviepy.audio.fx.all as afx
import fnmatch
import os
from PIL import Image

def get_comments():
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.tiff']
    images=[]
    files = os.listdir('./comments')
    sorted_files = sorted(files)
    for file in sorted_files:
        if any(fnmatch.fnmatch(file.lower(), ext) for ext in image_extensions):
            images.append("./comments/"+file)
    if len(images) == 0:
        print("images not found")
    print("images done")
    return images

def get_audios():
    print("getting audios")
    audios=[]
    files = os.listdir('./audios')
    sorted_files = sorted(files)
    for file in sorted_files:
        if fnmatch.fnmatch(file, '*.mp3'):
            print(file)
            audios.append("./audios/"+file)
    if len(audios) == 0:
        print("audios not found")
    return audios

def generate_video():

    images = get_comments()
    audios = get_audios()
    if (len(images)==0 or len(audios)==0)or(len(images)!=len(audios)):
        print("verify your files please!")
        return
    audio_clips=[]
    image_clips=[]
    bg_video = get_bg('*.mp4')
    video_Clip = VideoFileClip(bg_video)

    end_time = 0

    w_video, h_video = video_Clip.size

    for (c,a) in zip(images,audios):
        image_clip = configure_image(c,w_video,h_video)
        audio_clip = AudioFileClip(a).set_start(end_time)
        audio_clips.append(audio_clip)
        image_clips.append(image_clip.set_start(end_time)
                                     .set_pos("center", "center")
                                     .set_duration(audio_clip.duration)
                                     .set_audio(audio_clip))
        end_time = end_time + audio_clip.duration + 0.75
    
    if video_Clip.duration < end_time :
            video_Clip = video_Clip.fx(vfx.loop,duration=end_time + 0.75)
    else :
        video_Clip = video_Clip.subclip(0, end_time + 0.75)

    audio_final = CompositeAudioClip(
            [*audio_clips])
    video_Clip.audio = audio_final

    final_video_file = CompositeVideoClip(
            [video_Clip, *image_clips])
    
    # adding background music 

    secs=final_video_file.duration
    bg_audio = get_bg('*.mp3')
    back_audio = AudioFileClip(bg_audio).volumex(0.3)
    
    if back_audio.duration < secs :
        back_audio=afx.audio_loop(back_audio,duration=secs)
      
    final_audio = CompositeAudioClip([final_video_file.audio,back_audio])
    final_video_file = final_video_file.set_audio(final_audio)
    final_video_file = final_video_file.set_duration(secs)
        
    final_video_file.write_videofile("./finalvideo.mp4",
                              audio_codec='aac', fps=30, threads=4)

    

def configure_image(image,w_video,h_video):

    image_clip = ImageClip(image)
    margin = 20
    w_img , h_img = image_clip.size
    width_to_set = w_video - margin
    height_to_set = width_to_set * h_img / w_video

    image_clip = image_clip.resize(
        (width_to_set, height_to_set + 70),Image.Resampling.LANCZOS)
    
    return image_clip


def get_bg(ext):
    folder = ""
    if ext == "*.mp4":
        folder = "./bg_video"
    else :
        folder = "./bg_music"
    rslt=""
    listdir = os.listdir(folder)
    if len(listdir) != 0 :
        for file in listdir:
            if fnmatch.fnmatch(file.lower(), ext):
                print(file)
                rslt = os.path.join(folder, file)
                return rslt
    return rslt