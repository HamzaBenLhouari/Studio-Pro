import os
from pyfiglet import Figlet

def welcome_message():
    message = """
    ************************************
    *   Welcome to Video Studio Pro!   *
    ************************************

    This Python project is your one-stop solution for all things related to video creation and editing, text-to-speech integration, and AI-powered video production.

    Here’s what you can do with Video Studio Pro:

    1. **Video Editing**: Learn how to cut, merge, add effects, and more.
    2. **Text-to-Speech**: Use TikTok and ElevenLabs APIs to add speech to your videos.
    3. **Video Creation**: Practice creating educational, news, podcasts, and storytelling videos.
    We can add AI to this project to generate content based on PDF files
    To get started, explore the tutorials and examples provided in each section.
    """

    print(message)

if __name__ == "__main__":
    welcome_message()

    # Add more code here to guide users to the next steps
    print("\nNext Steps:")
    print("1. Navigate to the 'video_editing' folder to start with the video editing tutorials.")
    print("2. Check out the 'text_to_speech' folder for TTS integration.")
    print("3. Explore the 'video_creation' folder for practical video creation examples.")
    print("\nHappy Coding!")
    print(Figlet(font="cybermedium").renderText("Hamza Ben"))
