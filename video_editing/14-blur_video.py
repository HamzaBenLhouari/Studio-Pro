"""
14-input_blur_video
14-output_blur_video
"""
import os
import fnmatch
from moviepy.editor import VideoFileClip
from PIL import Image, ImageFilter
import numpy as np

def get_video():
    print("getting video")
    rslt=""
    folder = "./14-input_blur_video"
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
    
def blur_frame(image_frame):
    # Convert the frame (numpy array) to PIL Image
    pil_image = Image.fromarray(image_frame)
    
    # Apply Gaussian blur using PIL
    blurred_image = pil_image.filter(ImageFilter.GaussianBlur(radius=5))
    
    # Convert it back to a numpy array
    return np.array(blurred_image)

# Load video
video = get_video()
clip = VideoFileClip(video)

# Apply the blur function to all frames
blurred_clip = clip.fl_image(blur_frame)

# Save the resulting video
blurred_clip.write_videofile("./14-output_blur_video/1.mp4")
