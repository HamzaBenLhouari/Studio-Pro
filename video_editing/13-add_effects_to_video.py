"""
13-input_add_effects_to_video
13-output_add_effects_to_video
"""
from moviepy.editor import VideoFileClip
import moviepy.video.fx.all as vfx
import os
import fnmatch

def video_for_effects():
    print("getting video")
    rslt=""
    folder = "./13-input_add_effects_to_video"
    listdir = os.listdir(folder)
    if len(listdir) == 0 :
        print("video not found")
        return ""
    for file in listdir:
        if fnmatch.fnmatch(file.lower(), '*.mp4'):
            print(file)
            rslt = os.path.join(folder, file)
            print("video done")
            return rslt
    if rslt == "":
        return rslt
    
def main():
    video = video_for_effects()
    if video == "" :
        print("video not found")
        return
    video_Clip = VideoFileClip(video)
    
    # black and white
    #final_video_file = video_Clip.fx(vfx.blackwhite,RGB=None, preserve_luminosity=True)
    
    # decrease or increase the clip’s brightness 
    #final_video_file = video_Clip.fx(vfx.colorx,1.7)

    #crop the video
    #v_width, v_height = video_Clip.size
    #final_video_file = video_Clip.fx(vfx.crop, x1=None, y1=None, x2=None, y2=None, width=None, height=None, x_center=None, y_center=None)

    #Crops the clip to make dimensions even.
    #final_video_file = video_Clip.fx(vfx.even_size)

    #Gamma-correction of a video clip
    """
    This makes the video brighter.
    You can change this value according
    to the brightness level you want.
    NB: If you set gamma_value = 1, 
    there will be no change. 
    Values greater than 1 will darken the video.
    """
    #gamma_value = 0.5
    #final_video_file = video_Clip.fx(vfx.gamma_corr,gamma_value)

    #freeze  t=0,freeze_duration=None, total_duration=None, padding_end=0)
    #final_video_file = video_Clip.fx(vfx.freeze,t=3,freeze_duration=5, total_duration=None, padding_end=0)

    #Draws an external margin all around the frame
    # function margin(clip, mar=None, left=0, right=0, top=0, bottom=0, color=(0, 0, 0), opacity=1.0)
    #final_video_file = video_Clip.fx(vfx.margin,mar=None, left=50, right=50, top=100, bottom=100, color=(0, 0, 0), opacity=0.2)
    
    # flips the clip horizontally (and its mask too, by default)
    #final_video_file = video_Clip.fx(vfx.mirror_x, apply_to='mask')

    #flips the clip vertically (and its mask too, by default)
    #final_video_file = video_Clip.fx(vfx.mirror_y, apply_to='mask')


    #Transforms any photo into some kind of painting.
    # painting(clip, saturation=1.4, black=0.006)
    #final_video_file = video_Clip.fx(vfx.painting,saturation=1.4, black=0.006)

    """
    Changes the speed of the video by the given factor.
    A factor > 1 speeds up the video, 
    while a factor < 1 slows it down.
    """
    #speedx(clip, factor=None, final_duration=None)
    #final_video_file = video_Clip.fx(vfx.speedx, factor=2, final_duration=None)

    # Inverts the colors of the video
    #final_video_file = video_Clip.fx(vfx.invert_colors)

    # Rotates the video by a specified angle (in degrees)
    #final_video_file = video_Clip.fx(vfx.rotate, 90)

    # Reduces aliasing by rendering the video at a higher resolution 
    # and then downsampling it.
    #final_video_file = video_Clip.fx(vfx.supersample, 2, 10)

    # Adjusts the luminance and contrast of the video.
    final_video_file = video_Clip.fx(vfx.lum_contrast, lum=30, contrast=50)
    
    final_video_file.write_videofile("./13-output_add_effects_to_video/out.mp4",
                                    fps=30,
                                    remove_temp=True,
                                    codec="libx264",
                                    audio_codec="aac",
                                    threads = 6)
main()