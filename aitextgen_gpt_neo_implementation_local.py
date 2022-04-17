# -*- coding: utf-8 -*-
"""aitextgen GPT-NEO Implementation

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WPgw7I9al9ndt3v7vy7kFp4Rn3uYuVjG
"""

# Starter imports/setup

# !pip install -q aitextgen
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
import time
import re
import requests

import logging
logging.basicConfig(
        format="%(asctime)s — %(levelname)s — %(name)s — %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=logging.INFO
    )

from aitextgen import aitextgen
#from aitextgen.colab import mount_gdrive, copy_file_from_gdrive

# GPU Verification

# !nvidia-smi
"""
# ai = aitextgen(tf_gpt2="124M", to_gpu=True)
def run_setup():
    # Comment out the above line and uncomment the below line to use GPT Neo instead.
    ai = aitextgen(model="EleutherAI/gpt-neo-125M", to_gpu=True)

    mount_gdrive()

    file_name = "FullDataset.txt"

    # If caching is used, (UNUSED FOR THIS IMPLEMENTATION, FOR NOW!)
    #copy_file_from_gdrive(file_name)

    # Run the fine-tune

    ai.train(file_name,
             line_by_line=False,
             from_cache=False,
             num_steps=3000,
             generate_every=1000,
             save_every=1000,
             save_gdrive=True,
             learning_rate=1e-3,
             fp16=False,
             batch_size=1, 
             )

    # Load the trained model if one already exists

    from_folder = "/content/drive/MyDrive/Capstone Project/GOODONEATG_20220327_013515"

    for file in ["pytorch_model.bin", "config.json"]:
      if from_folder:
        copy_file_from_gdrive(file, from_folder)
      else:
        copy_file_from_gdrive(file)


    # Reload the model if just trained, makes it easier to use.

    # ai = aitextgen(model_folder="trained_model", to_gpu=True)

# ai.generate()
"""
def generation():
    keyFile = open('keys.txt', 'r')
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
    for post in allposts.json()['data']['children']:
             #print("Looking at Posts!")
             #Output all Keys to see available data.
             link = post['data']['url']
             if 'com' in link:
                 continue
             else:
                  if 'jpg' in link:
                     #print("Found an Image!")
                     image = link
                  else:
                      continue

    print(image)
    computerVision = ComputerVisionClient(AZURE_API_ENDPOINT, CognitiveServicesCredentials(AZURE_API_KEY))
    output = ""
    response = computerVision.describe_image(url=image, raw=True)
    #for tag in response.output.tags:
        #output += tag
        #output += ", "
    for caption in response.output.captions:
        output += caption.text
    detect = computerVision.detect_objects(image)
    #for obj in detect.objects:
       # print(obj.object_property, obj.rectangle)
    print(output)

    # load the retrained model + metadata necessary to generate text.
    ai = aitextgen(model_folder="GOODONEATG", to_gpu=False)

    ai.generate(n=5,
            batch_size=5,
            prompt=("Generate a compliment for " + output + ": \n"),
            max_length=45,
            temperature=0.75,
            top_p=0.9)