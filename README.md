# sdarot-py
cli tool for downloading series from sdarot.today

## Setup
install requirements:
```
pip install -r requirements.txt
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
Use "sid" code to download series (not specifing episodes downloads the whole season)
```
(venv) python main.py --sid=1774 -s=1-3
```

Use "out" to define output folder
```
(venv) python main.py --sid=1774 -s=1-3 -out="/Volume/SomeDisk/SomeFolder"
```

Default Output is set in the configuration.py and will be set to an "output" folder in the project root

Use "-i" code to bring interactive wizard to download multiple series with all seasons and episodes using series selection menu based on your search term
use space to select the series and enter to start the download
```
(venv) python main.py -gs "west"
```


## Run
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
(venv) python searchSeries.py [SEARCH_TERM]
```
```
(venv) python searchSeries.py game of thrones
```
Interactive multiple series download 
```
(venv) python main.py -gs "[SEARCH_TERM]"
```
```
(venv) python main.py -gs "west"
```