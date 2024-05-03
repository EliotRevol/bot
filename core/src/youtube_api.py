import os
import random
import string

import googleapiclient.discovery
import googleapiclient.errors


## @package youtube_api
#  Rêquetes à l'api youtube
#

## Fonction interne : Demander à l'api youtube un nombre définis de vidéo aléatoire.
# @param youtube Youtube API engine
# @param nb_required Nombre de vidéo aléatoire voulus.
# @return Vidéo json
def random_request(youtube, nb_required):
    random_val = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))
    requestVideo = youtube.search().list(
        part="snippet",
        q=random_val,
        type="video",
        maxResults=nb_required
    )
    responseVideo = requestVideo.execute()
    result = []
    for data in responseVideo['items']:
        video = {}
        # print(data)
        video['id'] = (data['id']['videoId'])
        video['title'] = (data['snippet']['title'])
        video['description'] = (data['snippet']['description'])
        video['channelId'] = (data['snippet']['channelId'])
        video['publishedAt'] = (data['snippet']['publishedAt'])
        video['channelTitle'] = (data['snippet']['channelTitle'])
        result.append(video)
    return result


## Demander à l'api youtube un nombre définis de vidéo aléatoire.
# @param nb_required Nombre de vidéo aléatoire voulus.
# @return Vidéo json
def get_randoms_videos(nb_required):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    api_key = "AIzaSyBXORLPJSsvclnHGD6fuVtwNW32jlDbQOc"

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)

    return random_request(youtube, nb_required)
