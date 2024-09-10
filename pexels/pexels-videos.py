import requests
import os

# Your Pexels API key
API_KEY = '0QsdDQy5jYrUXhonKtkKFdVr2oUsJCW9EyaYjBCOBOOGcbbVmA4P88wx'

# Set up the request headers with your API key
headers = {
    'Authorization': API_KEY,
}

# Define the search endpoint and parameters
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
