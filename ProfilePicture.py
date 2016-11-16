"""
Script to download a newspaper image and paste it into a profile picture.
"""

import base64
import datetime
import json
import os
import random
import shutil

import requests
from PIL import Image, ImageFilter
from twython import Twython


def get_newspaper_file(filename, slug='CAN_TGAM'):
    """
    Reach out to a newspaper, grab a picture and save it.
    """

    #This is hard-wired to grab the Globe and Mail.
    date_str = int(datetime.date.today().strftime("%d"))
    img_url = (
        'http://webmedia.newseum.org/newseum-multimedia/dfp/jpg{0}'
        '/lg/{1}.jpg').format(date_str, slug)

    print 'Getting url: ' + img_url
    resp = requests.get(img_url, stream=True)
    if resp.status_code == 200:
        with open(filename, 'wb') as out_file:
            resp.raw.decode_content = True
            shutil.copyfileobj(resp.raw, out_file)
    print 'Got it!'


def splice_image(newspaper_file, base_file, new_file):
    """
    Splice a new newspaper cover into the base picture.  Full of magic numbers.
    """

    print 'Splicing...'
    #Opens the two images:
    base_image = Image.open(base_file)
    page_image = Image.open(newspaper_file)

    #Blurs
    page_blurred = page_image.filter(ImageFilter.GaussianBlur(radius=1))
    page_blurred = page_blurred.resize(700, 1409)

    #Create a mask (invisible if >= 240 in greyscale)
    mask = page_image.convert('L')
    mask = Image.eval(mask, lambda x: 0 if x >= 240 else 255)

    #Paste into the base image and save.
    base_image.paste(page_blurred, (950, 110), mask=mask)
    to_save = base_image.resize((597, 600), Image.ANTIALIAS)
    to_save.save(new_file, 'JPEG', quality=90)
    print 'Spliced!'


def post_to_twitter(filename):
    """
    Posts the actual image to the twitters.
    Requires a keys.json file saved in the same directory, which looks like:
    {
        "app_key": "my_app_key",
        "app_secret": "my_app_secret",
        "oauth_token": "my_oauth_token",
        "oauth_token_secret": "my_oauth_token_secret"
    }
    """

    print 'Posting to twitter'
    with open('keys.json') as key_file:
        keys = json.load(key_file)

    #Grabs the connection to twitter
    twitter = Twython(
        keys['app_key'], keys['app_secret'], keys['oauth_token'],
        keys['oauth_token_secret'])

    with open(filename, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    _ = twitter.update_profile_image(image=encoded_string)
    print 'Posted!'


if __name__ == "__main__":

    NEWS_FILE = 'img/' + datetime.date.today().strftime("%Y%m%d") + '.jpg'
    NEW_FILE = 'newimage.jpg'
    BASE_FILE = 'baseimage.jpg'
    SLUG_CHOOSER = ('AZ_AR', 'CAN_TGAM')
    RANDOM_SLUG = random.choice(SLUG_CHOOSER)

    #Using this as a scheduled task, when the computer is on, then just
    #run it a bunch of times every day.
    if os.path.exists(NEWS_FILE):
        print 'Already done!!!'
    else:
        #Grabs the stuff
        get_newspaper_file(NEWS_FILE, slug=RANDOM_SLUG)
        splice_image(NEWS_FILE, BASE_FILE, NEW_FILE)
        post_to_twitter(NEW_FILE)
