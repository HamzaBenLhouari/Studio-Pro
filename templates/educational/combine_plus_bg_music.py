from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
import moviepy.audio.fx.all as afx
from pydub import AudioSegment
import os

def pad_audio_to_duration(audio_file, target_duration, output_audio_file):
    """
    Pads an audio file with silence to match a target duration.
    :param audio_file: Path to the audio file.
    :param target_duration: Target duration in seconds.
    :param output_audio_file: Path to save the padded audio.
    """
    # Load the audio file
    audio = AudioSegment.from_file(audio_file)
    current_duration = len(audio) / 1000  # Convert milliseconds to seconds

    if current_duration < target_duration:
        # Add silence to reach the target duration
        silence = AudioSegment.silent(duration=(target_duration - current_duration) * 1000)  # Convert to milliseconds
        padded_audio = audio + silence
    else:
        # Trim the audio if it's too long
        padded_audio = audio[:target_duration * 1000]

    # Export the padded audio
    padded_audio.export(output_audio_file, format="mp3")
    print(f"Padded audio saved as '{output_audio_file}'")

def combine_video_with_audio(video_file, main_audio_file, background_audio_file, output_file):
    """
    Combines a video with a main audio and background music.
    :param video_file: Path to the video file.
    :param main_audio_file: Path to the main audio file (padded).
    :param background_audio_file: Path to the background music file.
    :param output_file: Path for the output video file.
    """
    # Load the video and main audio clip
    video = VideoFileClip(video_file)
    main_audio = AudioFileClip(main_audio_file)

    # Load the background music
    background_audio = AudioFileClip(background_audio_file).volumex(0.3)  # Set volume to 30%

    # Loop the background music to match the video duration
    background_audio = afx.audio_loop(background_audio, duration=video.duration)
    
    # Combine both audios by overlaying them
    final_audio = main_audio.volumex(1.0).fx(lambda a: a.set_duration(video.duration))  # Main audio set to video duration
    final_audio = CompositeAudioClip([main_audio, background_audio])

    # Set the combined audio to the video
    final_video = video.set_audio(final_audio)

    # Export the final video
    final_video.write_videofile(output_file, codec='libx264', audio_codec='aac')
    print(f"Final video with synchronized audio and background music saved as '{output_file}'")

    os.remove(main_audio_file)

# Usage
video_file = "final_video.mp4"             # Path to your generated video file
original_audio_file = "final_audio.mp3"   # Path to the synchronized audio file
background_audio_file = "background.mp3"   # Path to the background music file
padded_audio_file = "padded_audio.mp3"     # Output path for the padded audio file
output_file = "final_output_with_audio.mp4"  # Path for the final output file

# Pad the main audio to match the video duration
video_duration = VideoFileClip(video_file).duration  # Get the video duration in seconds
pad_audio_to_duration(original_audio_file, video_duration, padded_audio_file)

# Combine the padded audio with the video and add background music
combine_video_with_audio(video_file, padded_audio_file, background_audio_file, output_file)