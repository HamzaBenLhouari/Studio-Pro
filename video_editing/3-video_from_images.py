"""
    You Need Input Files Here (Images)
    Put your Images in "3-input_video_from_images" directory 
    and wait the output video in 
    "3-output_video_from_images" directory
"""
import os
import fnmatch
from moviepy.editor import concatenate_videoclips, ImageClip, AudioFileClip

def fetch_images():
    print("getting videos")
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.tiff']
    images=[]
    # Folder containing images
    image_folder = "./3-input_video_from_images"
    for file in os.listdir(image_folder):
        if any(fnmatch.fnmatch(file.lower(), ext) for ext in image_extensions):
            print(file)
            images.append(os.path.join(image_folder, file))
    if len(images) == 0:
        return
    print("Images done")
    return images

def create_video_from_images(images):

    # Each image will be shown for 2 seconds 
    # You can change the duration 
    duration = 2
    clips = [ImageClip(img).set_duration(duration) for img in images]

    # Optionally add a crossfade transition between images
    crossfade_duration = 1  # Duration of crossfade in seconds
    clips = [clips[i].crossfadein(crossfade_duration) for i in range(len(clips))]

    # Concatenate the ImageClips into a single video clip
    video = concatenate_videoclips(clips, method="compose")

    # Write the final video to a file
    video.write_videofile("./3-output_video_from_images/out.mp4", fps=24, codec="libx264")

def main():

    images = fetch_images()
    
    if len(images) <= 1 :
        print("verify your files please! You must have more than one image")
        return
    
    create_video_from_images(images)

main()