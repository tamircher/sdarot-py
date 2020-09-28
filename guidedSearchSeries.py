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
hebrew_title_xpath = "./div/h4"
english_title_xpath = "./div/h5"
year_xpath = "./div/p/strong/following-sibling::text()"
genre_xpath = "./div/p[2]/strong/following-sibling::text()"

code_xpath = "./a"


def guided_search(search_term):
    print(Fore.YELLOW + f'Searching for: {Fore.YELLOW + Style.BRIGHT + search_term}\n')
    # search term
    res = requests.get(f'{Configuration.SDAROT_MAIN_URL}/search?term={search_term}')
    tree = html.fromstring(res.content)
    series_list = []
    response_url = res.url
    if response_url.find('/watch/') != -1:

        title: object = tree.xpath(title_single_res_path)[0].split(' / ')[1]
        series_code = response_url.split('/watch/', 1)[1].split('-', 1)[0]

        series_list.append({'label': title, 'code': series_code})
    else:

        elements = tree.xpath(element_xpath)

        for element in elements:
            eng_title = element.xpath(english_title_xpath)[0].text
            heb_title = element.xpath(hebrew_title_xpath)[0].text
            year = element.xpath(year_xpath)[0]
            genre = element.xpath(genre_xpath)[0]
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

    def extract_series_title(option):
        return f'[{option.get("year")}]   {option.get("eng_title")}  -  {get_display(option.get("heb_title"))}'

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
    guided_search(term)
