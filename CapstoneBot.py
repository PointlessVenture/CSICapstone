"""
Compliment Bot v 0.0.2
Aiden Tracy and Collin Westgate
Capstone 2022
"""


# Sources: https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c
# https://docs.microsoft.com/en-us/azure/cognitive-services/Computer-vision/quickstarts-sdk/client-library?pivots=programming-language-python&tabs=visual-studio
# https://www.youtube.com/watch?v=k8z-RbIBh68&ab_channel=JonWood


from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
import time
import re
import requests

keyFile = open('H:\Capstone\CSICapstone\keys.txt', 'r')
keyLines = keyFile.readlines()

AZURE_API_KEY = keyLines[0].rstrip()
AZURE_API_ENDPOINT = keyLines[1].rstrip()
REDDIT_CLIENT_ID = keyLines[2].rstrip()
REDDIT_SECRET_TOKEN = keyLines[3].rstrip()
REDDIT_UN = keyLines[4].rstrip()
REDDIT_PW = keyLines[5].rstrip()

# note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
auth = requests.auth.HTTPBasicAuth(REDDIT_CLIENT_ID, REDDIT_SECRET_TOKEN)

# here we pass our login method (password), username, and password
data = {'grant_type': 'password',
        'username': REDDIT_UN,
        'password': REDDIT_PW}

# setup our header info, which gives reddit a brief description of our app
headers = {'User-Agent': 'ComplimentBot/0.0.1'}

# send our request for an OAuth token
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

# convert response to JSON and pull access_token value
TOKEN = res.json()['access_token']

# add authorization to our headers dictionary
headers['Authorization'] = f'bearer {TOKEN}'

# while the token is valid (~2 hours) we just add headers=headers to our requests
print(headers)

allposts = requests.get('https://oauth.reddit.com/r/FreeCompliments/hot', headers=headers)
image = ''
file = open("testtext.txt","w")
for post in allposts.json()['data']['children']:
     #Output all Keys to see available data.
     #print(post['data'].keys())
     link = post['data']['url']
     if 'com' in link:
         continue
     else:
          if 'jpg' in link:
             image = link
             post_id = post['data']['id']
             sub = post['data']['subreddit']
             comment_URL = "https://oauth.reddit.com/r/" + sub + "/comments/" + post_id + "/irrelevant_string.json"
             comments = requests.get(comment_URL, headers=headers)
             #print(comments.json()[1]['data'])
             #print(comments.json()[0])
             print(image)
             file.write(image)
             file.write("\n")
             for comment in comments.json()[1]['data']['children']:
                #print(comment['data']['ups'])
                if comment['data']['ups'] >= 2:
                    print(comment['data']['body'])
                    file.write(comment['data']['body'])
                    file.write("\n")
             file.write("\n")
          else:
              continue

#image = "https://i.redd.it/vilrqew7rq481.jpg"
"""
print(image)
computerVision = ComputerVisionClient(AZURE_API_ENDPOINT, CognitiveServicesCredentials(AZURE_API_KEY))
output = ""
response = computerVision.describe_image(url=image, raw=True)
#print(dir(response))
#print(response.output)
#print(response.output.tags)
for tag in response.output.tags:
    output += tag
    output += ", "
for caption in response.output.captions:
    #print(caption.text, caption.confidence)
    output += caption.text
detect = computerVision.detect_objects(image)
#for obj in detect.objects:
   # print(obj.object_property, obj.rectangle)
print(output)

file.write(output)
"""
file.close()
