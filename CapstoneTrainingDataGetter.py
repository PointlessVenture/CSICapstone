"""
Compliment Bot v 0.0.2
Aiden Tracy and Collin Westgate
Capstone 2022
"""


# Sources: https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c
# https://docs.microsoft.com/en-us/azure/cognitive-services/Computer-vision/quickstarts-sdk/client-library?pivots=programming-language-python&tabs=visual-studio
# https://www.youtube.com/watch?v=k8z-RbIBh68&ab_channel=JonWood


#from azure.cognitiveservices.vision.computervision import ComputerVisionClient
#from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
#from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
#from msrest.authentication import CognitiveServicesCredentials
import time
import re
import requests

keyFile = open("keys.txt", "r")
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

afterstring = '?after='
allposts = ""

#To pull more data past first 2000: use lastID.txt file. Set variables accordingly.
lastID = ""
i = 0

if lastID != "":
    allposts = requests.get('https://oauth.reddit.com/r/FreeCompliments/top/?t=all' + afterstring + lastID, headers=headers)
else:
    allposts = requests.get('https://oauth.reddit.com/r/FreeCompliments/top/?t=all', headers=headers)

image = ''
j = i + 250000
next = ""
upvoteThreshold = 2
while i < j:
    #print("Looking at a request!")
    next = allposts.json()['data']['after']
    file = open("LastID.txt", "w")
    file.write(next)
    file.write("\n" + str(i))
    file.close()

    for post in allposts.json()['data']['children']:
         #print("Looking at Posts!")
         #Output all Keys to see available data.
         #print(post['data'].keys())
         link = post['data']['url']
         if 'com' in link:
             continue
         else:
                 #print("Found an Image!")
                 image = link
                 #print(image)
                 post_id = post['data']['id']
                 sub = post['data']['subreddit']
                 comment_URL = "https://oauth.reddit.com/r/" + sub + "/comments/" + post_id + ".json"
                 comments = requests.get(comment_URL, headers=headers)
                 #print(comments.json()[1]['data'])
                 #print(comments.json()[0])
                 #print(image)
                 #file.write(image)
                 #file.write("\n")
                 try:
                     for comment in comments.json()[1]['data']['children']:
                        #print(comment['data']['ups'])
                        try:
                            if comment['data']['ups'] >= upvoteThreshold:
                                #print("Found Comment #" + str(i))
                                if not (str(comment['data']['body'].encode('ascii', 'ignore'))[2:-1]).replace("\n", " ").__contains__("[]"):
                                    i = i + 1
                                    #print(comment['data']['body'])
                                    #print((str(comment['data']['body'].encode('ascii', 'ignore'))[2:-1]).replace("\n", " "))
                                    filename = "Compliments/compliment" + str(i) + ".txt"
                                    file = open(filename,"w")
                                    file.write((str(comment['data']['body'].encode('ascii', 'ignore'))[2:-1]).replace("\n", " "))
                                    file.write("\n")
                                    file.close()
                        except KeyError:
                            pass
                 except KeyError:
                    pass
                 #file.write("\n")
    nextUrl = 'https://oauth.reddit.com/r/FreeCompliments/top/?t=all' + '?after=' + next
    allposts = requests.get(nextUrl, headers=headers)

file = open("LastID.txt","w")
file.write(next)
file.write("\n" + str(i))
file.close()
