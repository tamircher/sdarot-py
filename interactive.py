import sys

import requests
from lxml import html
from colorama import init, Fore, Style
from configuration import Configuration
from pick import pick
from bidi.algorithm import get_display

init(autoreset=True)

title_single_res_path = "//div[@class='poster']//h1/strong/text()"
element_xpath = "//div[contains(@class,'sInfo')]"

single_hebrew_title_xpath = "//div[@class='poster']//h1/strong/text()"
single_english_title_xpath = "//div[@class='poster']//h1/strong/span/text()"
single_year_xpath = "//div[@id='year']/span/text()"
single_genre_xpath = "//div[@class='poster']//h3/strong/text()"

multi_hebrew_title_xpath = "./div/h4"
multi_english_title_xpath = "./div/h5"
multi_year_xpath = "./div/p/strong/following-sibling::text()"
multi_genre_xpath = "./div/p[2]/strong/following-sibling::text()"

code_xpath = "./a"


def interactive(search_term):
    print(Fore.YELLOW + f'Searching for: {Fore.YELLOW + Style.BRIGHT + search_term}\n')
    # search term
    res = requests.get(f'{Configuration.SDAROT_MAIN_URL}/search?term={search_term}')
    tree = html.fromstring(res.content)
    series_list = []
    response_url = res.url
    if response_url.find('/watch/') != -1:
        eng_title = tree.xpath(single_english_title_xpath)[0]
        heb_title = tree.xpath(single_hebrew_title_xpath)[0].rsplit('/', 1)[0]
        year = tree.xpath(single_year_xpath)[0]
        genre = tree.xpath(single_genre_xpath)[0].rsplit(':', 1)[1]
        # get series code from img src url
        series_code = response_url.split('/watch/', 1)[1].split('-', 1)[0]
        series_list.append({
            'eng_title': eng_title,
            'heb_title': heb_title,
            'year': year,
            'genre': genre,
            'code': series_code
        })

    else:

        elements = tree.xpath(element_xpath)

        for element in elements:
            eng_title = element.xpath(multi_english_title_xpath)[0].text
            heb_title = element.xpath(multi_hebrew_title_xpath)[0].text
            year = element.xpath(multi_year_xpath)[0]
            genre = element.xpath(multi_genre_xpath)[0]
            # get series code from img src url
            series_code = element.xpath(code_xpath)[0].get('href').rsplit('/', 1)[1].split('-', 1)[0]
            series_list.append({
                'eng_title': eng_title,
                'heb_title': heb_title,
                'year': year,
                'genre': genre,
                'code': series_code
            })

    title = 'Please choose a series to download completely (press SPACE to mark, ENTER to continue): '

    series_list.append({
        'eng_title': 'Exit without downloading',
        'heb_title': '',
        'year': 0,
        'genre': '',
        'code': -1
    })

    def extract_series_title(option):
        if option.get("code") != -1:
            return f'[{option.get("year")}]   {option.get("eng_title")}  -  {get_display(option.get("heb_title"))}'
        else:
            return f'>>>>> {option.get("eng_title")} <<<<<'

    selected = pick(
        options=series_list,
        title=title,
        multiselect=True,
        min_selection_count=1,
        indicator='*',
        options_map_func=extract_series_title,
    )
    return selected


if __name__ == "__main__":
    term = ' '.join(sys.argv[1:])
    interactive(term)
