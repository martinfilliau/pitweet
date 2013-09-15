import StringIO
import subprocess
import os
from random import choice
import time
from datetime import datetime, timedelta
from PIL import Image
from twython import Twython

IMG_FORMAT = 'png'

MESSAGES = ['Hello! #selfie #basil', 'Look at me! #selfpic #basil', 'Hi! #selfpic #basil']

BORN = datetime(2013, 9, 1)

def take_picture(flip=True):
    if flip:
        command = "raspistill -vf -w {width} -h {height} -t 0 -e {format} -o -".format(width=1000,
                                                                                    height=750,
                                                                                    format=IMG_FORMAT)
    else:
        command = "raspistill -w {width} -h {height} -t 0 -e {format} -o -".format(width=1000,
                                                                                    height=750,
                                                                                    format=IMG_FORMAT)
    imageData = StringIO.StringIO()
    imageData.write(subprocess.check_output(command, shell=True))
    imageData.seek(0)
    im = Image.open(imageData)
    buffer = im.load()
    imageData.close()
    image_io = StringIO.StringIO()
    im.save(image_io, format='JPEG')
    image_io.seek(0)
    return image_io
    
def tweet_picture(picture, message):
    twitter = Twython(get_consumer_key(), get_consumer_secret(), get_access_token(), get_access_token_secret())
    twitter.update_status_with_media(media=picture, status=message)

def tweet_normal():
    pic = take_picture(flip=True)
    tweet_picture(pic, get_message())
    
def tweet_go_wild():
    pic = take_picture(flip=False)
    tweet_picture(pic, "I'm going wild!")
    
def tweet_age():
    pic = take_picture(flip=True)
    age = datetime.now() - BORN
    message = "I was born {days} days ago!".format(days=age.days)
    tweet_picture(pic, message)

def get_message():
    return choice(MESSAGES)

def get_consumer_key():
    return get_kv('PITWEET_CONSUMER_KEY')
    
def get_consumer_secret():
    return get_kv('PITWEET_CONSUMER_SECRET')
    
def get_access_token():
    return get_kv('PITWEET_ACCESS_TOKEN')
    
def get_access_token_secret():
    return get_kv('PITWEET_CONSUMER_ACCESS_TOKEN_SECRET')
    
def get_kv(key):
    return os.getenv(key)
    
MODES = [tweet_normal, tweet_normal, tweet_normal, tweet_normal, tweet_age, tweet_age, tweet_go_wild]

if __name__ == '__main__':
    f = choice(MODES)
    f()