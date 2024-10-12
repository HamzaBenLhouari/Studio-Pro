import os, requests, base64, playsound
from moviepy.editor import AudioFileClip, VideoFileClip, ImageClip, CompositeVideoClip, CompositeAudioClip
import moviepy.video.fx.all as vfx
import moviepy.audio.fx.all as afx
import fnmatch


voice_type="en_us_009"
sessionid="20bd2616fae5f5592f824cf4f55f37fb"

def download_image(image,title):
    # Send a GET request to the URL
    response = requests.get(image)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Get the content of the response (the image data)
        image_data = response.content

        # Save the image data to a file
        with open("{}.jpg".format(title), "wb") as f:
            f.write(image_data)

        print("Image downloaded successfully")
        return "{}.jpg".format(title)
    else:
        print("Failed to download the image")
        return ""
    

def tts(session_id: str, text_speaker: str = "en_us_002", req_text: str = "TikTok Text To Speech", filename: str = 'voice.mp3', play: bool = False):

    req_text = req_text.replace("+", "plus")
    req_text = req_text.replace(" ", "+")
    req_text = req_text.replace("&", "and")

    headers = {
        'User-Agent': 'com.zhiliaoapp.musically/2022600030 (Linux; U; Android 7.1.2; es_ES; SM-G988N; Build/NRD90M;tt-ok/3.12.13.1)',
        'Cookie': f'sessionid={session_id}'
    }
    url = f"https://api22-normal-c-useast1a.tiktokv.com/media/api/text/speech/invoke/?text_speaker={text_speaker}&req_text={req_text}&speaker_map_type=0&aid=1233"
    r = requests.post(url, headers = headers)

    if r.json()["message"] == "Couldn't load speech. Try again.":
        output_data = {"status": "Session ID is invalid", "status_code": 5}
        print(output_data)
        return output_data

    vstr = [r.json()["data"]["v_str"]][0]
    msg = [r.json()["message"]][0]
    scode = [r.json()["status_code"]][0]
    log = [r.json()["extra"]["log_id"]][0]
    
    dur = [r.json()["data"]["duration"]][0]
    spkr = [r.json()["data"]["speaker"]][0]

    b64d = base64.b64decode(vstr)

    with open(filename, "wb") as out:
        out.write(b64d)

    output_data = {
        "status": msg.capitalize(),
        "status_code": scode,
        "duration": dur,
        "speaker": spkr,
        "log": log
    }

    print(output_data)

    if play is True:
        playsound.playsound(filename)
        os.remove(filename)

    return output_data


def generate_video(images,audios):
    audio_clips =[]
    image_clips = []
    bg_video = get_bg('*.mp4')
    video_Clip = VideoFileClip("./bg_video/backgroundvideo.mp4")

    end_time = 0

    w_video, h_video = video_Clip.size

    for (c,a) in zip(images,audios):
        image_clip = configure_image(c,w_video,h_video)
        a = AudioFileClip(a).set_start(end_time)
        if video_Clip.duration < (end_time + a.duration):
            video_Clip = video_Clip.fx(vfx.loop,duration=end_time + a.duration + 0.75)
        audio_clips.append(a.set_start(end_time))
        image_clips.append(image_clip.set_start(end_time)
                                     .set_pos("center", "center")
                                     .set_duration(a.duration)
                                     .set_audio(a))
            
        end_time = end_time + a.duration + 0.75
        
    video_Clip = video_Clip.subclip(0, end_time)

    """audio_final = CompositeAudioClip(
            [*audio_clips])
    video_Clip.audio = audio_final"""

    final_video_file = CompositeVideoClip(
            [video_Clip, *image_clips])
    
    # adding background music 

    """"secs=final_video_file.duration
    bg_audio = get_bg('*.mp3')
    back_audio = AudioFileClip("./backgroundmusic/oldnews.mp3").volumex(0.3)
    
    if back_audio.duration < secs :
        back_audio=afx.audio_loop(back_audio,duration=secs)
      
    back_audio=back_audio.volumex(0.5)
    final_audio = CompositeAudioClip([final_video_file.audio,back_audio])
    final_video_file = final_video_file.set_audio(final_audio)
    final_video_file = final_video_file.set_duration(secs)
        """
    final_video_file.write_videofile("./finalvideo.mp4",
                              audio_codec='aac', fps=30, threads=4)

    

def configure_image(image,w_video,h_video):

    image_clip = ImageClip(image)
    margin = 20
    w_img , h_img = image_clip.size
    width_to_set = w_video - margin
    height_to_set = width_to_set * h_img / w_video

    image_clip = image_clip.resize(
        (width_to_set, height_to_set + 70))
    
    return image_clip


def get_bg(ext):
    folder = ""
    if ext == "*.mp4":
        folder = "./bg_video"
    else :
        folder = "./bg_music"
    rslt=""
    listdir = os.listdir(folder)
    if len(listdir) == 0 :
        print("logo not found")
        return ""
    for file in listdir:
        if fnmatch.fnmatch(file.lower(), ext):
            print(file)
            rslt = os.path.join(folder, file)
            return rslt
    if rslt == "":
        return