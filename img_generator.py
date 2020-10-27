# Tested on Python 3.6.1, 3.7.7

# install: pip install --upgrade arabic-reshaper
import arabic_reshaper
# install: pip install python-bidi
from bidi.algorithm import get_display
# install: pip install Pillow
from PIL import Image, ImageDraw, ImageFont

import json
import urllib.request

with open(r'tmp/tweet.json', encoding='utf8') as json_file:
    data = json.load(json_file)
    for p in data:
        user_name = p['user']['name']
        profile = p['user']['profile_image_url']
        tweet_content = p['tweet']['full_text']


# themes
# def theme(img, font):

# use a good font!
fontFile = "./assets/font/sahel/sahel.ttf"

# a 1080x1920 jpg file
imageFile = "./assets/images/input/tweetNegar.jpg"

# load the profile photo
# profile = Image.open("./assets/user/profile.jpg")
urllib.request.urlretrieve(profile, "./assets/user/profile0.jpg") # Save Profile Photo
user_profile = Image.open("./assets/user/profile0.jpg")
profile = user_profile.resize((180, 180))

# load the font and image
font = ImageFont.truetype(fontFile, 50)
image = Image.open(imageFile)

# firts you must prepare your text (you dont need this for english text)
username = user_name
reshaped_text = arabic_reshaper.reshape(username)    # correct its shape
bidi_name = get_display(reshaped_text)

# tweet content
text =  tweet_content[:40] + '\n' + tweet_content[40:80] + '\n' + tweet_content[80:120] + '\n' + tweet_content[120:160] + '\n' + tweet_content[160:200] + '\n' + tweet_content[200:240] + '\n' + tweet_content[240:280]
# Content Should Wrap in a Better Way, this is just for test!!

reshaped_text = arabic_reshaper.reshape(text)    # correct its shape
bidi_text = get_display(reshaped_text)           # correct its direction

# get image size
(w, h) = image.size

# text location
cx = w//2
cy = h//2

# start drawing on image
draw = ImageDraw.Draw(image)
draw.text((400, 650), bidi_name, (25, 25, 100), font=font, spacing=0, align='right')

draw.multiline_text((300, 850), bidi_text, fill='black', font=font, spacing=10, align='right')

draw = ImageDraw.Draw(image)

# draw profile photo on output
mask = Image.new("L", profile.size, 0)
draw = ImageDraw.Draw(mask)
draw.ellipse((0, 0, 180, 180), fill=255)
mask.save("./assets/user/mask.jpg")
image.paste(profile, (755, 595), mask)

# save it
image.save("./assets/images/output/tweetNegar0.png")
