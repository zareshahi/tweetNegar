# Tested on Python 3.6.1, 3.7.7

# install: pip install --upgrade arabic-reshaper
import arabic_reshaper
# install: pip install python-bidi
from bidi.algorithm import get_display
# install: pip install Pillow
from PIL import Image, ImageDraw, ImageFont
# preinstalled in python
import urllib.request
# preinstalled in python
import textwrap
# preinstalled in python
import json

# read json file
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
urllib.request.urlretrieve(profile, "./assets/user/profile0.jpg") # Save Profile Photo from twitter
user_profile = Image.open("./assets/user/profile0.jpg") # load profile photo
profile = user_profile.resize((180, 180))

# load the font and theme image
font = ImageFont.truetype(fontFile, 50)
image = Image.open(imageFile)

# firts you must prepare your text (you dont need this for english text)
username = user_name
reshaped_text = arabic_reshaper.reshape(username)    # correct its shape
bidi_name = get_display(reshaped_text)

# tweet content
# Content Should Wrap in a Better Way, this is just for test!!
my_wrap = textwrap.TextWrapper(width = 30)
wrap_list = my_wrap.wrap(text=tweet_content)
text = ''

reshaped_text = arabic_reshaper.reshape(text)    # correct its shape
bidi_text = get_display(reshaped_text)           # correct its direction

# get image size
(w, h) = image.size

# text location
cx = w//2
cy = h//2

# start drawing on image
draw = ImageDraw.Draw(image)

draw.text((400, 650), bidi_name, (25, 25, 100), font=font, spacing=0, align='left')

th = 850
for text in wrap_list:
    reshaped_text = arabic_reshaper.reshape(text)    # correct its shape
    bidi_text = get_display(reshaped_text)           # correct its direction
    draw.multiline_text((240, th), bidi_text, fill='black', font=font, spacing=10, align='left')
    th = th + 60 # space between each line

draw = ImageDraw.Draw(image)

# draw profile photo on output
mask = Image.new("L", profile.size, 0)
draw = ImageDraw.Draw(mask)
draw.ellipse((0, 0, 180, 180), fill=255)
mask.save("./assets/user/mask.jpg")
image.paste(profile, (755, 595), mask)

# save it
image.save("./assets/images/output/tweetNegar0.png")
