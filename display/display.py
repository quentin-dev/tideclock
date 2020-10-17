import logging

from PIL import Image, ImageDraw, ImageFont

from .waveshare_epd import epd2in13_V2


class Display:
    def __init__(self):
        logging.info("Initializing Display")
        self.epd = epd2in13_V2.EPD()
        logging.info("Initialized Display EPD")

    def epd_clear(self):
        """Clear the e-ink display"""
        logging.info("Clearing Display EPD")
        self.epd.init(self.epd.FULL_UPDATE)
        self.epd.Clear(0x00)
        self.epd.Clear(0xFF)

    def epd_sleep(self):
        """Put e-ink display to sleep"""
        logging.info("Putting Display EPD to sleep")
        self.epd.sleep()

    def epd_display_text(self, text):
        """Display given text centered on the e-ink display"""
        image = Image.new("1", (self.epd.height, self.epd.width), 255)
        draw = ImageDraw.Draw(image)

        font = ImageFont.truetype("fonts/Roboto-Bold.ttf", 18)

        w, h = draw.textsize(text, font=font)

        draw.text(
            ((self.epd.height - w) // 2, (self.epd.width - h) // 2),
            text,
            fill=0,
            font=font,
        )
        self.epd.display(self.epd.getbuffer(image))

    def epd_display(self, subtitle, title="Prochaine marée :", fontSize=24):
        """Display title and subtitle centered on the e-ink display"""

        image = Image.new("1", (self.epd.height, self.epd.width), 255)
        draw = ImageDraw.Draw(image)

        font = ImageFont.truetype("fonts/Roboto-Bold.ttf", fontSize)

        titleW, titleH = draw.textsize(title, font=font)
        subW, subH = draw.textsize(subtitle, font=font)

        baseH = (self.epd.width - (titleH + subH)) // 2

        draw.text(((self.epd.height - titleW) // 2, baseH), title, fill=0, font=font)
        draw.text(
            ((self.epd.height - subW) // 2, baseH + titleH), subtitle, fill=0, font=font
        )

        self.epd.display(self.epd.getbuffer(image))
