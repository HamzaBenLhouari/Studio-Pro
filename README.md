# Studio Pro

### Created by Hamza Ben L'houari (Hamza Ben)

---

## Table of Contents

1. [Project Description](#project-description)
2. [Features](#features)
3. [Getting Started](#getting-started)
   - [1. Clone and Install Dependencies](#1-clone-and-install-dependencies)
   - [2. Set Up API Keys](#2-set-up-api-keys)
   - [3. Configure Environment Variables](#3-configure-environment-variables)
     - [TikTok Session ID](#tiktok-session-id)
   - [4. Additional Setup](#4-additional-setup)
4. [Folder Structure](#folder-structure)
   - [video_editing](#video_editing)
   - [tts](#tts)
   - [pexels](#pexels)
   - [templates](#templates)
5. [Special Thanks](#special-thanks)

---

## Project Description

**Studio Pro** is a comprehensive Python solution for video editing, text-to-speech integration, and versatile video production workflows. Whether you’re a creator, developer, or hobbyist, Studio Pro offers a range of tools to enhance your multimedia projects.

### Features:

- **Video Editing**: Step-by-step tutorials for video cutting, merging, adding effects, and more.
- **Text-to-Speech (TTS)**: Seamlessly integrate voiceovers with TikTok and ElevenLabs APIs.
- **Pexels Integration**: Fetch high-quality images and videos using the Pexels API.
- **Templates**: Ready-to-use templates for educational, news, podcasting, and storytelling videos.
- **AI-Powered Content Creation** (Planned Feature): Future AI capabilities for PDF-based content generation and automated video responses.

---

## Getting Started

### 1. Clone and Install Dependencies

To install required packages, run:

```bash
pip install -r requirements.txt
```

### 2. Set Up API Keys

Create accounts and get API keys from the following platforms:

- **Pexels**: pexels.com
- **ElevenLabs**: elevenlabs.io
- **News API**: newsapi.org

### 3. Configure Environment Variables

1. Rename .env.example to .env in the root folder.
2. Enter your API keys in the .env file as follows

   ```bash
   TIKTOK_SESSION_ID=<your_tiktok_session_id>
   PEXELS_API_KEY=<your_pexels_api_key>
   ELEVENLABS_API_KEY=<your_elevenlabs_api_key>
   NEWS_API_KEY=<your_news_api_key>
   ```

#### TikTok Session ID

To obtain the TikTok sessionid:

Connect to TikTok.
Press F12 for Developer Tools, go to Network, select www.tiktok.com, navigate to Cookies, and locate sessionid.

### 4. Additional Setup

Download and install ImageMagick and MikTeX for image processing and LaTeX support in video creation.

## Folder Structure

### video_editing

Tutorials and example scripts for video manipulation, each with corresponding input/output folders.

### tts

Scripts for text-to-speech using TikTok and ElevenLabs, organized by tiktok and elevenlabs subfolders.

- tiktok:

  - voices.py: Lists available voices.
  - tiktok-tts.py: Main TTS processing script.
  - helper_conf_tts.py: A helper script.
  - tiktok_tts/: Contains:
    - script.txt: Enter the script here, separating sections with ## (each section must be under 300 characters).
    - voice_model.txt: Specify the voice model code.
  - output_tiktok_tts: Outputs are saved here as .mp3 file.

- elevenlabs:

  - elevenlabs_tts.py: Main script for ElevenLabs TTS processing.
  - helper_config.py: A helper script.
  - eleven_labs_tts/: Contains:
    - script.txt: Enter the script, separating sections with ##.
    - voice_model.txt: Specify the voice model name (available on ElevenLabs).
  - output_eleven_labs_tts: Outputs are saved here as .mp3 file.

### pexels

Scripts for downloading images and videos from Pexels. Configure search parameters directly in each script.

- pexels-images.py: Script to retrieve images based on user-defined parameters (query, per_page, and page).
- pexels-videos.py: Script to retrieve videos with similar parameters.
- Retrieved files are saved in the images and videos folders.

### templates

Practical templates for specific use cases:
comments: Creates a narrated video based on comment images.
educational: Generates educational videos with or without background audio.
news: Builds news videos by fetching the latest headlines.
podcast: Produces a podcast-style video with multiple speakers.
story: Creates story-based videos using pre-structured scripts and images.
Each folder contains instructions on usage and configuration.

- templates: Contains five customizable video creation folders:

  - comments:

    - Structure: Folders (audios, comments, bg_music, bg_video) and files (helper.py, main.py).
    - Use: Place comment images in comments, background video in bg_video, audio files in audios, and background music in bg_music.
    - Requirements: Ensure the number of files in comments and audios match. The script in main.py synchronizes the audio and images to create a video.

  - educational:

    - Structure: background.mp3 file (replaceable, but must retain the same name), read.ms file for usage instructions.
    - Output: Generated media folder contains the final video in video. After generating, rename the file to final_video.mp4 and run combine_plus_bg_music.py to add background music.

  - news:

    - Structure: helper.py, main.py, and folders (audios, images, bg_video, bg_music).
    - Customization: Modify topheadlines in main.py to change the news source (e.g., bbc-news, us, or bitcoin) and set news_number.
    - Output: main.py creates a news video using TikTok TTS and images.

  - podcast:

    - Structure: main.py, helper.py, and folders (audios, image, bg_music, script).
    - Use: Add script text in script/script.txt (separate sections with ##), an image in image, and background music in bg_music.
    - Output: main.py generates a podcast-style video.

  - story:
    - Structure: silence.mp3 (for pauses between speech segments), main.py, helper.py, and folders (audios, images, script, bg_music).
    - Use: Add story text in script/script.txt (separate frames with ##, separate speakers within a frame with $$). Match the number of frames with images for visual synchronization.
    - Output: Generates a story video with sequential audio-visual segments.

## Special Thanks

A heartfelt thank you to all the developers and contributors who made this project possible. We extend our gratitude to the open-source community for libraries like MoviePy, Pillow, NumPy, ElevenLabs, TikTok, Pexels, News API, and all other libraries used in this project. Each tool and API contributed significantly to making Studio Pro versatile and robust.

Thank you also to all contributors on GitHub who generously share solutions, insights, and enhancements, and to the creators of essential software like ImageMagick and MiKTeX. Your work inspires creativity, collaboration, and innovation across the global developer community.

Happy Coding! 😊
