# sdarot-py
cli tool for downloading series from sdarot.today

## Setup
create virtual environment
```
python -m venv venv
```
install requirements inside venv:
```
(venv) pip install -r requirements.txt
```

## Usage
Search for "sid" by title
```
(venv) python main.py --search "rick"
Searching for: rick
Rick and Morty - 1774
Party Tricks - 1794
Patrick Melrose - 3968
```
Use "sid" code to download serie (not specifing episodes downloads the whole season)
```
(venv) python main.py --sid=1774 -s=1-3
```

Output will be in the "output" folder in the project root

## Run
Inside venv

Download
```
(venv) python main.py --sid=[SERIES_ID] -s=[SEASON_NUMBER_START]-[SEASON_NUMBER_END] -e=[EPISODE_NUMBER_START]-[EPISODE_NUMBER_END]
```
```
(venv) python main.py --sid=1774 -s=1-3 -e=1-12
```

Search
```
(venv) python main.py --search "[SEARCH_TERM]"
```
```
(venv) python main.py --search "westworld"
```
or
```
(venv) python searchSerie.py [SEARCH_TERM]
```
```
(venv) python searchSerie.py game of thrones
```
