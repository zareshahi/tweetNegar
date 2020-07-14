# Tested on Python 3.6.1

# install: pip install --upgrade arabic-reshaper
import arabic_reshaper
# install: pip install python-bidi
from bidi.algorithm import get_display
# install: pip install Pillow
from PIL import Image, ImageDraw, ImageFont

# use a good font!
fontFile = "./assets/font/sahel/sahel.ttf"

# a 1080x1920 jpg file
imageFile = "./assets/images/input/tweetNegar.jpg"

# load the profile photo
profile = Image.open("./assets/user/profile.png") 

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

draw.multiline_text((300, 850), bidi_text, fill='black', font=font, spacing=10, align='right')

draw = ImageDraw.Draw(image)

# draw profile photo on output
mask = Image.new("L", profile.size, 0)
draw = ImageDraw.Draw(mask)
draw.ellipse((0, 0, 180, 180), fill=255)
mask.save("./assets/user/mask.jpg")
image.paste(profile, (755, 595), mask)

# save it
image.save("./assets/images/output/tweetNegar.png")
