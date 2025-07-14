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

    # Precompute sizes of rotated text lines
    rotated_line_heights = []
    rotated_line_widths = []

    for line in haiku:
        bbox = font.getbbox(line)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        # After rotation, width and height swap
        rotated_w, rotated_h = h, w
        rotated_line_heights.append(rotated_h)
        rotated_line_widths.append(rotated_w)

    # Calculate total height for vertical centering
    total_rotated_text_height = sum(rotated_line_heights)
    start_y = (epd.height - total_rotated_text_height) // 2

    current_y = start_y

    # Draw each rotated line centered horizontally and stacked vertically
    for i, line in enumerate(haiku):
        w = rotated_line_widths[i]
        h = rotated_line_heights[i]

        # Create temp image for horizontal text line (before rotation)
        text_img = Image.new('1', (h, w), 255)  # swap w,h for rotation
        text_draw = ImageDraw.Draw(text_img)
        text_draw.text((0, 0), line, font=font, fill=0)

        # Rotate text image -90 degrees clockwise
        rotated_text_img = text_img.rotate(-90, expand=True)

        # Center horizontally on display
        x = (epd.width - rotated_text_img.width) // 2

        # Paste rotated text onto correct color layer
        if i == 1:
            image_red.paste(rotated_text_img, (x, current_y))
        else:
            image_black.paste(rotated_text_img, (x, current_y))

        # Move y offset down for next line
        current_y += rotated_text_img.height
        
    epd.display(epd.getbuffer(image_black), epd.getbuffer(image_red))

    time.sleep(15)
    epd.Clear()
    epd.sleep()

except KeyboardInterrupt:
    epd2in13b_V4.epdconfig.module_exit(cleanup=True)

