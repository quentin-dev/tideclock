#!/usr/bin/env python3

import argparse
import csv
import logging
import sys
import time
from datetime import date

import display


def getRowFromCSV(filename, rowNum):
    """Get a specific row from a given file"""

    with open(filename) as file:

        reader = csv.reader(file)

        rows = [row for ndx, row in enumerate(reader) if ndx == rowNum]

    return rows[0]


def getDataForToday():
    """Get TideData for today's date"""

    today = date.today()

    ndx = today.toordinal() - date(today.year, 1, 1).toordinal() + 1
    row = getRowFromCSV(f"data/{today.year}.csv", ndx)

    # Create Data

    return row


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog="tideclock",
        description="Display the current tides on a waveshare e-ink screen",
    )

    parser.add_argument(
        "--dry-run", action="store_true", help="Run without fetching or displaying data"
    )

    parser.add_argument(
        "--mode",
        type=str,
        choices=["debug", "production"],
        default="debug",
        help="Set logging level",
    )

    args = parser.parse_args()

    loglevel = logging.ERROR if args.mode == "production" else logging.DEBUG

    logging.basicConfig(level=loglevel)
    logging.info("Starting tideclock")

    data = getDataForToday()

    if args.dry_run:

        print(data)
        sys.exit()

    display = display.Display()

    display.epd_clear()
    display.epd_display_text("This is a test")
    time.sleep(10)
    display.epd_clear()
