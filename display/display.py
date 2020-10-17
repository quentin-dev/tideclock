import logging

from PIL import Image, ImageDraw, ImageFont

from .waveshare_epd import epd2in13_V2


class Display:
    def __init__(self):
        logging.info("Initializing Display")
        self.epd = epd2in13_V2.EPD()
        logging.info("Initialized Display EPD")

    def epd_clear(self):
        logging.info("Clearing Display EPD")
        self.epd.init(self.epd.FULL_UPDATE)
        self.epd.Clear(0xFF)

    def epd_sleep(self):
        logging.info("Putting Display EPD to sleep")
        self.epd.sleep()

    def epd_display_text(self, text):
        image = Image.new("1", (self.epd.height, self.epd.width), 255)
        draw = ImageDraw.Draw(image)

        font = ImageFont.truetype("fonts/Roboto-Bold.ttf", 18)

        draw.text((0, self.epd.width // 2), text, fill=0, font=font)
        self.epd.display(self.epd.getbuffer(image))


"""
image = Image.new('1', (epd.height, epd.width), 255)
draw = ImageDraw.Draw(image)

# draw.text((120, 60), "Kdo pour Papa", fill = 0)

draw.text((0, 60), weather.get_tides_from_meteofrance()[0], fill = 0)

# draw.rectangle([(0, 0), (50, 50)], outline = 0)
epd.display(epd.getbuffer(image))
# time.sleep(10)

logging.info("Clear")
# epd.init(epd.FULL_UPDATE)
# epd.Clear(0xFF)
# epd.sleep()
"""
