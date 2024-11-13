import requests
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Description:
# This script searches for videos on Pexels using their API and downloads the results.
# The search query, result count per page, and page number can be customized.
# Results are saved in a "videos" directory in the current working directory.
# To use this script, create a .env file with your Pexels API key:
#     PEXELS_API_KEY='your_api_key_here'

# Retrieve the Pexels API key from environment variables
API_KEY = os.getenv('PEXELS_API_KEY')
if not API_KEY:
    raise ValueError("API key not found. Please add it to a .env file as PEXELS_API_KEY='your_api_key_here'")

# Set up the request headers with the API key
headers = {
    'Authorization': API_KEY,
}

# Define the search endpoint and parameters for videos
search_url = 'https://api.pexels.com/videos/search'
params = {
    'query': 'nature',  # Search query
    'per_page': 5,      # Number of results per page
    'page': 1           # Page number
}

# Make the request to the Pexels API
response = requests.get(search_url, headers=headers, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    
    # Create a directory to save the videos
    if not os.path.exists('videos'):
        os.makedirs('videos')

    # Download each video
    for i, video in enumerate(data['videos']):
        video_url = video['video_files'][0]['link']
        video_response = requests.get(video_url)

        if video_response.status_code == 200:
            with open(f'videos/video_{i+1}.mp4', 'wb') as file:
                file.write(video_response.content)
            print(f'Downloaded video_{i+1}.mp4')
        else:
            print(f'Failed to download video_{i+1}')
else:
    print(f'Error: {response.status_code}')
