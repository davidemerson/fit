import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'eink')
if os.path.exists(libdir):
    sys.path.append(libdir)

from eink import epd2in13_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

try:
    epd = epd2in13_V2.EPD()

    font15 = ImageFont.truetype("futura_pt_heavy.ttf", 15)
    font36 = ImageFont.truetype("futura_pt_heavy.ttf", 36)
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)

    epd.init(epd.FULL_UPDATE)
    epd.displayPartBaseImage(epd.getbuffer(time_image))

    epd.init(epd.PART_UPDATE)
    num = 0
    while (True):
        time_draw.rectangle((0, 0, 220, 105), fill = 255)
        time_draw.text((0, 0), time.strftime('%H:%M:%S'), font = font36, fill = 0)
        epd.displayPartial(epd.getbuffer(time_image))
        num = num + 1
        if(num == 5):
            break

    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)

    epd.sleep()

except KeyboardInterrupt:
    epd2in13_V2.epdconfig.module_exit()
    exit()