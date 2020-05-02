import requests
from itertools import product

sids = [''.join(sid) for sid in product('0123456789', repeat=4)]
serie_exists = []


def url(sid): return f'https://sdarot.today/watch/{sid}'


def get_last_serie(arr, bot, top):

    while bot < top:

        mid = (bot + top) // 2

        is_exists = requests.head(url(arr[mid])).status_code == 200
        print(arr[mid], is_exists)

        # If x is greater, ignore left half
        if is_exists:
            bot = mid + 1

        # If x is smaller, ignore right half
        else:
            top = mid - 1

    is_exists = requests.head(url(arr[bot])).status_code == 200
    sid = bot - (0 if is_exists else 1)
    print(arr[mid], is_exists)
    return sid


get_last_serie(sids, 0, len(sids))
