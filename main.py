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
    font_size = 14
    font = ImageFont.truetype(font_path, font_size)

    # Generate haiku
    haiku = generate_haiku()

    # Measure line height using textbbox
    bbox = draw_black.textbbox((0, 0), "A", font=font)
    line_height = bbox[3] - bbox[1]

    # Vertical centering
    total_text_height = line_height * len(haiku)
    start_y = (epd.height - total_text_height) // 2
    
    # Draw haiku lines rotated by -90 degrees
    for i, line in enumerate(haiku):
        # Get text size
        bbox = font.getbbox(line)  # alternative to textbbox for font only
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Create temp image for the text line (white background)
        text_img = Image.new('1', (text_width, text_height), 255)
        text_draw = ImageDraw.Draw(text_img)
        text_draw.text((0, 0), line, font=font, fill=0)

        # Rotate text image -90 degrees (clockwise)
        rotated_text_img = text_img.rotate(-90, expand=True)
        rotated_w, rotated_h = rotated_text_img.size

        # Center horizontally (along epd.width)
        x = (epd.width - rotated_w) // 2

        # Distribute vertically based on line index
        y = start_y + i * rotated_h

        if i == 1:
            image_red.paste(rotated_text_img, (x, y))
        else:
            image_black.paste(rotated_text_img, (x, y))

    epd.display(epd.getbuffer(image_black), epd.getbuffer(image_red))

    time.sleep(15)
    epd.Clear()
    epd.sleep()

except KeyboardInterrupt:
    epd2in13b_V4.epdconfig.module_exit(cleanup=True)

