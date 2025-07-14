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
    image_black = Image.new('1', (epd.width, epd.height), 255)
    image_red = Image.new('1', (epd.width, epd.height), 255)

    draw_black = ImageDraw.Draw(image_black)
    draw_red = ImageDraw.Draw(image_red)

    # Load font
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(BASE_DIR, 'fonts', 'Quintessential-Regular.ttf')
    font_size = 28
    font = ImageFont.truetype(font_path, font_size)

    # Generate haiku
    haiku = generate_haiku()

    # Measure line height using textbbox
    bbox = draw_black.textbbox((0, 0), "A", font=font)
    line_height = bbox[3] - bbox[1]

    # Vertical centering
    total_text_height = line_height * len(haiku)
    start_y = (epd.height - total_text_height) // 2

    # Draw haiku lines
    for i, line in enumerate(haiku):
        bbox = draw_black.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        x = (epd.width - w) // 2
        y = start_y + i * line_height

        if i == 1:
            draw_red.text((x, y), line, font=font, fill=0)  # red layer (middle line)
        else:
            draw_black.text((x, y), line, font=font, fill=0)  # black layer
    
    # Display
    epd.display(epd.getbuffer(image_black), epd.getbuffer(image_red))

    time.sleep(15)
    epd.Clear()
    epd.sleep()

except KeyboardInterrupt:
    epd2in13b_V4.epdconfig.module_exit(cleanup=True)

