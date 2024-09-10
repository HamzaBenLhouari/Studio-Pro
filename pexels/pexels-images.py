import requests
import os

# Your Pexels API key
API_KEY = '0QsdDQy5jYrUXhonKtkKFdVr2oUsJCW9EyaYjBCOBOOGcbbVmA4P88wx'

# Set up the request headers with your API key
headers = {
    'Authorization': API_KEY,
}

# Define the search endpoint and parameters
search_url = 'https://api.pexels.com/v1/search'
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
    
    # Create a directory to save the images
    if not os.path.exists('images'):
        os.makedirs('images')

    # Download each photo
    for i, photo in enumerate(data['photos']):
        image_url = photo['src']['original']
        image_response = requests.get(image_url)

        if image_response.status_code == 200:
            with open(f'images/photo_{i+1}.jpg', 'wb') as file:
                file.write(image_response.content)
            print(f'Downloaded photo_{i+1}.jpg')
        else:
            print(f'Failed to download photo_{i+1}')
else:
    print(f'Error: {response.status_code}')
