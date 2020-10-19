# tideclock

A Python utility to print the next high / low tide to a Waveshare e-ink screen
on RPi Zero (W)

## Warning

This utility is made to be used with an RPi Zero (W) and a Waveshare e-ink
display, so it will probably not work on any other hardware

## Development

This project uses `black`, `flake8`, `isort`, and `pre-commit` in order to
provide a fully functional development environment.

## Installation

1) `python -m venv venv`
2) `. venv/bin/activate`
3) `pip install -r requirement.txt`
4) `pre-commit install`
5) `./tidescraper.py --help`

## Options

|     Name     | Short Option |         Long Option          |                       Description                       | Default Value |
|:------------:|:------------:|:----------------------------:|:-------------------------------------------------------:|:-------------:|
|     Help     |     `-h`     |           `--help`           |                 Shows help information                  |     NONE      |
|     Mode     |     NONE     | `--mode {debug, production}` |                   Sets logging level                    |    `debug`    |
|   Dry Run    |     NONE     |         `--dry-run`          |           Displays data in INFO log and exits           |     NONE      |
|     Demo     |     NONE     |           `--demo`           |   Displays data to screen, then wait, clear, and exit   |     NONE      |
| Time To Wait |     NONE     |         `--ttw TTW`          | Sets time to wait, only taken into account in demo mode |     `10`      |
