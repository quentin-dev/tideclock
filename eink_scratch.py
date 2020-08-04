#!/usr/bin/env python3

import sys
import os
import logging
import traceback
import time

from waveshare_epd import epd2in13_V2
from PIL import Image, ImageDraw, ImageFont

logging.basicConfig(level=logging.DEBUG)

logging.info("eink scratch")

epd = epd2in13_V2.EPD()
logging.info("Init & Clear")
epd.init(epd.FULL_UPDATE)
epd.Clear(0xFF)

image = Image.new('1', (epd.height, epd.width), 255)
draw = ImageDraw.Draw(image)

draw.text((120, 60), "Kdo pour Papa", fill = 0)

# draw.rectangle([(0, 0), (50, 50)], outline = 0)
epd.display(epd.getbuffer(image))
time.sleep(10)

logging.info("Clear")
epd.init(epd.FULL_UPDATE)
epd.Clear(0xFF)
epd.sleep()
