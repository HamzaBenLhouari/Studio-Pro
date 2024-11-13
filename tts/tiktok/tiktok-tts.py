"""
Ensure each paragraph in 'script.txt' is separated by "##".
Each paragraph should be under 300 characters.
"""

from helper_conf_tiktok import get_script, get_voice_type, tts
from moviepy.editor import concatenate_audioclips, AudioFileClip
import time
from dotenv import load_dotenv
import os

def generate_final_voice(session_id, voice_type, script):
    """
    Generates a final voice clip by splitting the script, generating audio for each part,
    and concatenating the audio files.
    
    Args:
        session_id (str): The session ID for TikTok API access.
        voice_type (str): The selected voice model type.
        script (str): The full script text, with paragraphs separated by "##".
    """
    # Split the script by "##" to create separate paragraphs
    voices = script.split("##")
    audio_files = []

    # Generate audio for each paragraph
    for i, voice in enumerate(voices, start=1):
        output_path = f"./output_tiktok_tts/voice{i}.mp3"
        tts(session_id, voice_type, voice, output_path, False)
        time.sleep(5)  # Prevent API rate limits
        audio_files.append(output_path)
    
    # Concatenate all audio clips into a final audio file
    audio_clips = [AudioFileClip(c) for c in audio_files]
    final_clip = concatenate_audioclips(audio_clips)
    final_clip.write_audiofile("./output_tiktok_tts/voice.mp3")
    print("Generated audio files:", audio_files)

def main():
    """
    Main function to load environment variables, retrieve script and voice type,
    and generate the final voice output.
    """
    # Load environment variables from a .env file
    load_dotenv()
    
    # Retrieve TikTok session ID from environment variables
    session_id = os.getenv('TIKTOK_SESSION_ID')
    if not session_id:
        raise ValueError("API key not found. Please add it to a .env file as TIKTOK_SESSION_ID='your_api_key_here'")
    
    # Retrieve the script and voice type
    script = get_script()
    if not script:
        print("No script found. Exiting.")
        return
        
    voice_type = get_voice_type()
    if not voice_type:
        print("No voice type found. Exiting.")
        return
    
    # Generate final voice output
    generate_final_voice(session_id, voice_type, script)

if __name__ == "__main__":
    main()
