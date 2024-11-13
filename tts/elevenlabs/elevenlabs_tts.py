from elevenlabs import set_api_key,generate, save
from helper_config import get_text, get_voice_model
from moviepy.editor import concatenate_audioclips, AudioFileClip
import time
from dotenv import load_dotenv
import os

def main():
    """Generate audio files from text using the Eleven Labs API and save as a single concatenated MP3."""
    
    # Load environment variables from a .env file
    load_dotenv()
    
    # Retrieve the API key from environment variables
    api_key = os.getenv('ELEVEN_LABS_KEY')
    if not api_key:
        raise ValueError("API key not found. Please add it to a .env file as ELEVEN_LABS_KEY='your_api_key_here'")
    set_api_key(api_key)
    
    # Retrieve text and voice model
    my_text = get_text()
    if not my_text:
        print("No text found; terminating process.")
        return
    
    voice_model = get_voice_model()
    if not voice_model:
        print("No voice model found; terminating process.")
        return
    
    # Split the text script and initialize audio file list
    segments = my_text.split("##")
    audio_files = []
    
    # Generate audio for each text segment and save
    for idx, segment in enumerate(segments, start=1):
        print(f"Processing segment {idx}...")

        # Generate audio for the current text segment
        audio = generate(
            text=segment,
            voice=voice_model,
            model="eleven_multilingual_v2"
        )
        
        # Define and save the output file for the current audio
        file_path = f"./output_eleven_labs_tts/voice_{idx}.mp3"
        save(audio, file_path)
        
        # Pause to ensure API call stability
        time.sleep(5)
        audio_files.append(file_path)

    # Concatenate all audio clips
    print("Concatenating audio files...")
    audio_clips = [AudioFileClip(file) for file in audio_files]
    final_clip = concatenate_audioclips(audio_clips).volumex(1.7)
    final_clip.write_audiofile("./output_eleven_labs_tts/voice.mp3")

    print("Process completed: Final audio saved as voice.mp3")

if __name__ == "__main__":
    main()