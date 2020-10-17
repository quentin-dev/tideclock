#!/usr/bin/env python3

import argparse
import csv
import logging
import sys
import time
from datetime import date, datetime
from enum import Enum
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


def getNextEvent(data: List[str], today) -> Tuple[str, datetime.time]:
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

    current = datetime.now().time()

    upcoming = [elt for elt in valid if elt[1] >= current]

    # FIXME: Does not account for the case where the next event is tomorrow

    return upcoming[0]


def getData(today) -> List[str]:
    """Get TideData for a given date"""

    ndx = today.toordinal() - date(today.year, 1, 1).toordinal() + 1
    row = getRowFromCSV(f"data/{today.year}.csv", ndx)

    logging.debug(f"Got row {row}")

    return row


def getNextEventForToday() -> Tuple[str, datetime.time]:
    """Get next high / low tide event for today"""

    today = date.today()
    data = getData(today)

    return getNextEvent(data, today)


def eventToString(event: Tuple[str, datetime.time]) -> str:

    tideType = "basse" if event[0][:2] == "LT" else "haute"

    return f"Prochaine marée {tideType} à {event[1].strftime('%Hh%M')}"


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

    event = getNextEventForToday()
    eventString = eventToString(event)

    if args.dry_run:

        logging.debug(eventString)
        sys.exit()

    display = display.Display()

    display.epd_clear()
    display.epd_display_text(eventString)
    time.sleep(10)
    display.epd_clear()
