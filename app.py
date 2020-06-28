import arabic_reshaper
import numpy as np
from bidi.algorithm import get_display
from PIL import Image, ImageDraw, ImageFont

# Make canvas and set the color
img = np.zeros((1920, 1080, 3), np.uint8)
b, g, r, a = 0, 255, 0, 0

# Initial path's
vazir_font_path = './assets/font/vazir/Vazir-Light.ttf'
instagram_story_path = './assets/images/output/insta_storty.jpeg'

# firts you must prepare your text (you dont need this for english text)
text = "بسم الله الرحمان الرحیم"
reshaped_text = arabic_reshaper.reshape(text)    # correct its shape
bidi_text = get_display(reshaped_text)           # correct its direction


# Use vazir font
vazir_font = ImageFont.truetype(vazir_font_path, 24)
instagram_story = Image.open(instagram_story_path)

draw = ImageDraw.Draw(instagram_story)

img_pil = Image.fromarray(img)
draw = ImageDraw.Draw(img_pil)
draw.text((img.shape[1]//2, img.shape[0]//2),
          bidi_text, font=vazir_font, fill=(b, g, r, a))
img = np.array(img_pil)

img_pil.show()
