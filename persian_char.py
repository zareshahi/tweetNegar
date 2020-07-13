# Tested on Python 3.6.1

# install: pip install --upgrade arabic-reshaper
import arabic_reshaper
# install: pip install python-bidi
from bidi.algorithm import get_display
# install: pip install Pillow
from PIL import Image, ImageDraw, ImageFont

# use a good font!
fontFile = "Sahel.ttf"

# this was a 400x400 jpg file
imageFile = "input.jpg"

# load the font and image
font = ImageFont.truetype(fontFile, 18)
image = Image.open(imageFile)

# firts you must prepare your text (you dont need this for english text)
text = "سلام ایران"
reshaped_text = arabic_reshaper.reshape(text)    # correct its shape
bidi_text = get_display(reshaped_text)           # correct its direction

# start drawing on image
draw = ImageDraw.Draw(image)
draw.text((0, 0), bidi_text, (255, 255, 255), font=font)
draw = ImageDraw.Draw(image)

# save it
image.save("output.png")
