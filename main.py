import os
import time
from PIL import Image, ImageDraw, ImageFont
from lib import epd2in13b_V4
from haiku_gen import generate_haiku

try:
    epd = epd2in13b_V4.EPD()
    epd.init()
    epd.Clear()

    # Create separate images for black and red
    image_black = Image.new('1', (250, 122), 255)
    image_red = Image.new('1', (250, 122), 255)

    draw_black = ImageDraw.Draw(image_black)
    draw_red = ImageDraw.Draw(image_red)

    # Load font
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(BASE_DIR, 'fonts', 'Roboto.ttf')
    font_size = 16
    font = ImageFont.truetype(font_path, font_size)

    # Generate haiku
    haiku = generate_haiku().splitlines()

    draw_black.text((8, 18), f"{haiku[0]}", font = font, fill = 0)
    draw_red.text((8, 51), f"{haiku[1]}", font = font, fill = 0)
    draw_black.text((8, 84), f"{haiku[2]}", font = font, fill = 0)
    draw_red.rectangle((2, 2, 247, 119), outline=0)

    # Display
    epd.display(epd.getbuffer(image_black), epd.getbuffer(image_red))
    time.sleep(15)
    epd.Clear()
    epd.sleep()

except KeyboardInterrupt:
    epd2in13b_V4.epdconfig.module_exit(cleanup=True)

