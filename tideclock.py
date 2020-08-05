#!/usr/bin/env python3

import sys
# import os
import logging
# import traceback
# import time

import weather

import argparse

# from display import Display

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog = 'tideclock',
        description = 'Display the current tides on a waveshare e-ink screen'
    )

    parser.add_argument(
        '--dry-run',
        action = 'store_true',
        help = 'Run without fetching or displaying data'
    )

    parser.add_argument(
        '--mode',
        type = str,
        choices = [ 'debug', 'production' ],
        default = 'debug',
        help = 'Set logging level'
    )

    args = parser.parse_args()

    if args.dry_run:
        sys.exit()

    from display import Display

    loglevel = logging.ERROR if args.mode == 'production' else logging.DEBUG

    logging.basicConfig(level = loglevel)
    logging.info("Starting tideclock")

    text = weather.get_tides_from_meteofrance()

    display = Display()
    
    display.epd_clear()
    display.epd_display_text(text[0])

