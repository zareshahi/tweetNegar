from io import BytesIO
import arabic_reshaper
from bidi.algorithm import get_display
from numpy import array, uint8, zeros
from PIL import Image, ImageDraw, ImageFont

def build_image(text="بسم الله الرحمن الرحیم",font_size=24,font_path='./assets/font/vazir/Vazir-Light.ttf',image_path='./assets/images/output/insta_storty.jpeg'):

    # Make canvas and set the color
    # TODO: use flexible size by user input
    img = zeros((1920, 1080, 3), uint8)
    b, g, r, a = 0, 255, 0, 0


    # firts you must prepare your text (you dont need this for english text)
    # TODO: change text size by text length
    reshaped_text = arabic_reshaper.reshape(text)    # correct its shape
    bidi_text = get_display(reshaped_text)           # correct its direction


    # Use vazir font
    vazir_font = ImageFont.truetype(font_path, font_size)

    end_image = Image.open(image_path)
    draw = ImageDraw.Draw(end_image)
    w, h = draw.textsize(text.encode('utf8'))

    # Add text on image
    draw.text(((img.shape[1]-w)/2, (img.shape[0]-h)/2),
            bidi_text, font=vazir_font, fill=(b, g, r, a))

    return end_image

def get_image(id):
    # save image to memory for send to telegram bot
    bio = BytesIO()
    bio.name = f'image{id}.jpeg'
    img = build_image()
    img.save(bio, 'JPEG')
    bio.seek(0)
    return bio
