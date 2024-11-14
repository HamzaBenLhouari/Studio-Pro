from newsapi import NewsApiClient
from helper import tts, generate_video, download_image
import time
import os
from dotenv import load_dotenv
import sys

# Ensure environment variables are loaded
load_dotenv()

# Retrieve sessionid from the .env file
sessionid = os.getenv('TIKTOK_SESSION_ID')

# Retrieve new_api_key from the .env file
new_api_key = os.getenv('NEWS_API_KEY')

if not sessionid or not new_api_key:
    print("Error: TIKTOK_SESSION_ID OR NEWS_API_KEY not found in .env file.")
    sys.exit()

# The voice 
voice_type="en_us_009"

api = NewsApiClient(api_key=new_api_key)

topheadlines = api.get_top_headlines(sources='bbc-news')
#topheadlines = api.get_top_headlines(country='us')
#bitcoin=api.get_everything(q='bitcoin')
#sources = api.get_sources()

images=[]
audios=[]
NEWS_NUMBER=5
if 'articles' in topheadlines:
    # Iterate over each article
    count=1
    for article in topheadlines['articles']:
        # Extract desired fields
        title = article.get('title', 'No title available')
        author = article.get('author', 'No author available')
        description = article.get('description', 'No description available')
        image_url = article.get('urlToImage', 'No image available')
        file_name="news_{}".format(count)

        if image_url != "No image available":
            image = download_image(image_url,file_name)
            print(image_url)
            print(image)
            images.append(image)
        else:
            print("No image available")
        #if title&description&author!='no X available'
        script= title+". "+description
        time.sleep(10)
        tts(sessionid,voice_type,script,"./audios/{}.mp3".format(file_name),False)
        time.sleep(10)
        audios.append("./audios/{}.mp3".format(file_name))
    
        if count == NEWS_NUMBER :
            break
        count=count+1

else:
    print("No 'articles' key found in the JSON data")

generate_video(images,audios)

for (c,a) in zip(images,audios):
    os.remove(c)
    os.remove(a)