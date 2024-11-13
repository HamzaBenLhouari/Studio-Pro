"""
You Need Input Files Here (Audios)
Put your Audios in "7-input_concatenate_audios" directory 
and wait for the output audio in 
"7-output_concatenate_audios" directory
You can set a volume value for the final audio
    search volumex() 
"""
import os
import fnmatch
from moviepy.editor import AudioFileClip, concatenate_audioclips

# Constants for directories and output file
INPUT_DIR = "./7-input_concatenate_audios"
OUTPUT_DIR = "./7-output_concatenate_audios"
OUTPUT_FILENAME = "out.mp3"

def fetch_audios():
    print("Fetching audio files...")
    audios = []
    for file in os.listdir(INPUT_DIR):
        if fnmatch.fnmatch(file, '*.mp3'):
            print(f"Found audio file: {file}")
            audios.append(os.path.join(INPUT_DIR, file))
    if not audios:
        print("No audio files found.")
    return audios

def concatenate_audios(audios):
    audio_clips = [AudioFileClip(audio).volumex(1.7) for audio in audios]
    final_audio = concatenate_audioclips(audio_clips)

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Write the final concatenated audio
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)
    final_audio.write_audiofile(output_path)
    print(f"Concatenated audio saved to {output_path}")

def main():
    audios = fetch_audios()
    
    if len(audios) <= 1:
        print("Please verify! You must have more than one audio file.")
        return
    
    concatenate_audios(audios)

if __name__ == "__main__":
    main()
