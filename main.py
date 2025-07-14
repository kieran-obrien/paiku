import os
import time
from PIL import Image, ImageDraw, ImageFont
from lib import epd2in13b_V4
from haiku_gen import generate_haiku

try:
    epd = epd2in13b_V4.EPD()
    epd.init()
    epd.Clear()

    # Prepare image and drawing context
    image_black = Image.new('1', (epd.width, epd.height), 255)  # White background
    image_red = Image.new('1', (epd.width, epd.height), 255)    # Also white background

    draw_black = ImageDraw.Draw(image_black)
    draw_red = ImageDraw.Draw(image_red)

    # Load your font (adjust path and size)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(BASE_DIR, 'fonts', 'Quintessential-Regular.ttf')
    font_size = 28
    font = ImageFont.truetype(font_path, font_size)

    # Your haiku lines
    haiku = generate_haiku()

    # Calculate vertical spacing for 3 lines centered nicely
    line_height = font.getsize("A")[1]  # height of one line
    total_text_height = line_height * len(haiku)
    start_y = (epd.height - total_text_height) // 2

    # Draw each line centered horizontally
    for i, line in enumerate(haiku):
        w, h = draw_black.textsize(line, font=font)  # Use either draw here just for measuring
        x = (epd.width - w) // 2
        y = start_y + i * line_height

    if i == 1:
        draw_red.text((x, y), line, font=font, fill=0)   # red layer
    else:
        draw_black.text((x, y), line, font=font, fill=0) # black layer

    # Display both buffers
    epd.display(epd.getbuffer(image_black), epd.getbuffer(image_red))

    time.sleep(10)
    epd.Clear()
    epd.sleep()

except KeyboardInterrupt:
    epd2in13b_V4.epdconfig.module_exit(cleanup=True)
