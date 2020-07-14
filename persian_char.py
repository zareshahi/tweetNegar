# Tested on Python 3.6.1

# install: pip install --upgrade arabic-reshaper
import arabic_reshaper
# install: pip install python-bidi
from bidi.algorithm import get_display
# install: pip install Pillow
from PIL import Image, ImageDraw, ImageFont

# use a good font!
fontFile = "./assets/font/sahel/sahel.ttf"

# this was a 400x400 jpg file
imageFile = "./assets/images/input/tweetNegar.jpg"

# load the font and image
font = ImageFont.truetype(fontFile, 50)
image = Image.open(imageFile)

# firts you must prepare your text (you dont need this for english text)
username = "نام توئیت کننده"
reshaped_text = arabic_reshaper.reshape(username)    # correct its shape
bidi_name = get_display(reshaped_text)

text = """متن متن متن متن متن 
متن متن متن متن متن
متن متن متن متن متن"""

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

draw.multiline_text((300, 850), bidi_text, fill='purple', font=font, spacing=10, align='center')

draw = ImageDraw.Draw(image)

# save it
image.save("./assets/images/output/tweetNegar.png")
