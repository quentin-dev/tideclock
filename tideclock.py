#!/usr/bin/env python3

import sys
# import os
import logging
# import traceback
import time
import argparse

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

    # An attempt at something, will probably be moved with the other imports
    import display

    loglevel = logging.ERROR if args.mode == 'production' else logging.DEBUG

    logging.basicConfig(level = loglevel)
    logging.info("Starting tideclock")

    display = display.Display()
    
    display.epd_clear()
    display.epd_display_text("This is a test")
    time.sleep(10)
    display.epd_clear()

