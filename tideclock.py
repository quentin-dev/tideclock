#!/usr/bin/env python3

import argparse
import csv
import logging
import sys
import time
from datetime import date, datetime
from datetime import time as dttime
from datetime import timedelta
from enum import Enum
from pathlib import Path
from typing import List, Tuple

import display


class TideTime(Enum):
    HTM = 2
    HTN = 3
    LTM = 4
    LTN = 5


def getRowFromCSV(filename: str, rowNum: int) -> List[str]:
    """Get a specific row from a given file"""

    logging.info(f"Going to attempt to open {filename}@{rowNum}")

    with open(filename) as file:

        reader = csv.reader(file)

        rows = [row for ndx, row in enumerate(reader) if ndx == rowNum]

    return rows[0]


def getNextEvent(data: List[str], day, tomorrow=False) -> Tuple[str, datetime]:
    """Get the next high / low tide event"""

    valid = []

    for event in TideTime:

        try:

            tmp = datetime.strptime(data[event.value].strip(), "%H:%M")

            logging.debug(f"Successfully parsed '{data[event.value].strip()}' as time")

            valid.append((event.name, tmp.time()))

        except ValueError:

            logging.debug(f"Failed parsing '{data[event.value].strip()}' as time")

    valid.sort(key=lambda x: x[1])

    # If the next event is tomorrow set the current time to midnight

    current = dttime(0, 0, 0) if tomorrow else datetime.now().time()

    upcoming = [elt for elt in valid if elt[1] >= current]

    return (upcoming[0][0], datetime.combine(day, upcoming[0][1]))


def getData(today) -> List[str]:
    """Get TideData for a given date"""

    ndx = today.toordinal() - date(today.year, 1, 1).toordinal() + 1
    row = getRowFromCSV(Path(__file__).parent / f"data/{today.year}.csv", ndx)

    logging.debug(f"Got row {row}")

    return row


def getNextEventForToday() -> Tuple[str, datetime]:
    """Get next high / low tide event for today"""

    try:

        today = date.today()
        data = getData(today)

        logging.info(f"Going to get next event for {today}")

        return getNextEvent(data, today)

    except IndexError:

        logging.info(f"The last event of {today} has passed")

        tomorrow = today + timedelta(days=1)
        data = getData(tomorrow)

        logging.info(f"Going to get earliest event of {tomorrow}")

        return getNextEvent(data, tomorrow, True)


def eventToString(event: Tuple[str, datetime.time]) -> str:

    tideType = "BASSE" if event[0][:2] == "LT" else "HAUTE"

    return f"{tideType} à {event[1].strftime('%Hh%M')}"


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog="tideclock",
        description="Display the current tides on a waveshare e-ink screen",
    )

    parser.add_argument(
        "--dry-run", action="store_true", help="Display data in INFO log and exit"
    )

    parser.add_argument(
        "--demo",
        action="store_true",
        help="Display data to screen, then wait, clear, and exit",
    )

    parser.add_argument(
        "--ttw",
        type=int,
        default=10,
        help="Set time to wait, only taken into account in demo mode",
    )

    parser.add_argument(
        "--mode",
        type=str,
        choices=["debug", "production"],
        default="debug",
        help="Set logging level",
    )

    args = parser.parse_args()

    loglevel = logging.INFO if args.mode == "production" else logging.DEBUG

    logging.basicConfig(level=loglevel)
    logging.info("Starting tideclock")

    display = display.Display()

    while True:

        event = getNextEventForToday()
        eventString = eventToString(event)

        # Wait an extra minute to avoid sleeping for 0 seconds
        ttw = (event[1] - datetime.now()).total_seconds() + 60

        if args.dry_run:

            logging.info(f"Got event string '{eventString}'")
            sys.exit()

        display.epd_clear()
        display.epd_display(eventString)

        if args.demo:

            time.sleep(args.ttw)
            display.epd_clear()

            sys.exit()

        logging.info(f"Going to sleep for {ttw} seconds")

        time.sleep(ttw)
