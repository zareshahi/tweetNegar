from io import BytesIO

import arabic_reshaper
from bidi.algorithm import get_display
from numpy import array, uint8, zeros
from PIL import Image, ImageDraw, ImageFont

# Make canvas and set the color
# TODO: use flexible size by user input
img = zeros((1920, 1080, 3), uint8)
b, g, r, a = 0, 255, 0, 0

# Initial path's
# TODO: use config.json and import more fonts
vazir_font_path = './assets/font/vazir/Vazir-Light.ttf'
instagram_story_path = './assets/images/output/insta_storty.jpeg'

# firts you must prepare your text (you dont need this for english text)
# FIXME: get text from user by get_text() function
text = "بسم الله الرحمان الرحیم"
# TODO: change text size by text length
reshaped_text = arabic_reshaper.reshape(text)    # correct its shape
bidi_text = get_display(reshaped_text)           # correct its direction


# Use vazir font
vazir_font = ImageFont.truetype(vazir_font_path, 24)
instagram_story = Image.open(instagram_story_path)

draw = ImageDraw.Draw(instagram_story)

img_pil = Image.fromarray(img)
draw = ImageDraw.Draw(img_pil)
w, h = draw.textsize(text.encode('utf8'))
draw.text(((img.shape[1]-w)/2, (img.shape[0]-h)/2),
          bidi_text, font=vazir_font, fill=(b, g, r, a))
img = array(img_pil)


def get_image(id):
    # save image to memory for send to telegram bot
    bio = BytesIO()
    bio.name = f'image{id}.jpeg'
    img_pil.save(bio, 'JPEG')
    bio.seek(0)
    return bio


def set_text(text):
    text = text
