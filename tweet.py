import StringIO
import subprocess
import os
import time
from datetime import datetime
from PIL import Image
from twython import Twython

IMG_FORMAT = 'png'

def take_picture():
    command = "raspistill -vf -w {width} -h {height} -t 0 -e {format} -o -".format(width=1000,
                                                                                    height=750,
                                                                                    format=IMG_FORMAT)
    imageData = StringIO.StringIO()
    imageData.write(subprocess.check_output(command, shell=True))
    imageData.seek(0)
    im = Image.open(imageData)
    buffer = im.load()
    imageData.close()
    return im
    
def tweet_picture():
    pic = take_picture()
    image_io = StringIO.StringIO()
    pic.save(image_io, format='JPEG')
    image_io.seek(0)
    twitter = Twython(get_consumer_key(), get_consumer_secret(), get_access_token(), get_access_token_secret())
    twitter.update_status_with_media(media=image_io, status='Hello! #selfie #basil')

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
    
if __name__ == '__main__':
    tweet_picture()