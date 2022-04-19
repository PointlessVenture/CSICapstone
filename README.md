# CSICapstone  
Aiden Tracy and Collin Westgate

## Compliment Bot
The purpose of this capstone project is to create a bot capable of producing tailored compliments to images pulled from the r/FreeCompliments subreddit.

It utilizes:

A fine-tuned *GPT-NEO* model via the *aitextgen* tool.  
*Microsoft Computervision* to describe images for the model to give compliments to.  
The *Reddit API* for getting images and compliment data for fine-tuning.  

Colab Implementation (primarily used for fine-tuning the dataset):
https://colab.research.google.com/drive/1WPgw7I9al9ndt3v7vy7kFp4Rn3uYuVjG?usp=sharing

## Setup
Download the repository, using whichever method you prefer.

Download the Model, which can be found in the "Link to Dataset.txt" file, or at https://drive.google.com/drive/folders/1OdlgVSJY9KTG8tn2nFaPEMfpvqW7DA1A?usp=sharing.
  Alternatively, use the Colab Implementation above to create your own Model from a dataset of your choosing.
  
Run, in the directory in which the bot will run, the following command:
# pip install -r prereqs.txt
This will download all nessesary python modules.

Follow the instructions in samplekeys.txt, to generate keys.txt.

Run main.py.
