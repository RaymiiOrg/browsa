# Browsa.py

Little Python script which browses random websites, to make it harder for spying entities to extract data points and signals from monitoring.

## Installation

    pip install bs4

## Usage

    browsa.py URL
    browsa.py https://raymii.org

## Requirements

- Python 2.7
- Beautifulsoup 4

## Pitfalls

The script crashes with non-unicode characters in the URL. Because it is quick and dirty just use this quick and dirty fix:

    while true; do ./browsa.py https://raymii.org/; sleep 30; done

