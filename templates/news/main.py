from newsapi import NewsApiClient
from helper import tts, generate_video, download_image, sessionid, voice_type
import time
import os
#my_api_key='902b84a90473457c8778e40f163e4259'
api = NewsApiClient(api_key='902b84a90473457c8778e40f163e4259')

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