from newsapi import NewsApiClient
from helper import tts, generate_video, download_image, sessionid, voice_type
import time
import os

api = NewsApiClient(api_key='902b84a90473457c8778e40f163e4259')

topheadlines = api.get_top_headlines(sources='bbc-news')
#topheadlines = api.get_top_headlines(country='us')
#bitcoin=api.get_everything(q='bitcoin')
#sources = api.get_sources()

images=[]
audios=[]
if 'articles' in topheadlines:
    # Iterate over each article
    for article in topheadlines['articles']:
        # Extract desired fields
        title = article.get('title', 'No title available')
        author = article.get('author', 'No author available')
        description = article.get('description', 'No description available')
        image_url = article.get('urlToImage', 'No image available')

        # Print the extracted fields
        """print("Title:", title)
        print("Author:", author)
        print("Description:", description)
        print("Image URL:", image_url)
        print()"""
        #
        if image_url != "No image available":
            image = download_image(image_url,title)
            images.append(image)
        else:
            print("No image available")
        #if title&description&author!='no X available'
        script= title+". "+description
        time.sleep(10)
        tts(sessionid,voice_type,script,"./audios/{}.mp3".format(title),False)
        time.sleep(10)
        audios.append("./audios/{}.mp3".format(title))
        

else:
    print("No 'articles' key found in the JSON data")

generate_video(images,audios)

for (c,a) in zip(images,audios):
    os.remove(c)
    os.remove(a)