import os

def get_text():
    """Retrieve and return the text script from a file if available."""
    file_path = "./eleven_labs_tts/script.txt"
    
    # Check if file exists before attempting to read
    if not os.path.exists(file_path):
        print("Script file not found.")
        return ""
    
    with open(file_path, 'r') as f:
        script = f.read().strip()
    
    if script:
        print("Text script loaded successfully.")
    else:
        print("Script is empty.")
    
    return script

def get_voice_model():
    """Retrieve and return the voice model from a text file if available."""
    file_path = "./eleven_labs_tts/voice_model.txt"
    
    # Check if file exists before attempting to read
    if not os.path.exists(file_path):
        print("Voice model file not found.")
        return ""
    
    with open(file_path, 'r') as f:
        voice_model = f.read().strip()
    
    if voice_model:
        print("Voice model loaded successfully.")
    else:
        print("Voice model is empty.")
    
    return voice_model
