import sys

import requests
from lxml import html
from colorama import init, Fore, Style
from configuration import Configuration

init(autoreset=True)

title_single_res_path = "//div[@class='poster']//h1/strong/text()"
element_xpath = "//div[contains(@class,'sInfo')]"
english_title_xpath = "./div/h5"
code_xpath = "./a"


def search(search_term):

    print(Fore.YELLOW + f'Searching for: {Fore.YELLOW + Style.BRIGHT + search_term}\n')
    # search term
    res = requests.get(f'{Configuration.SDAROT_MAIN_URL}/search?term={search_term}')
    tree = html.fromstring(res.content)

    response_url = res.url
    if response_url.find('/watch/') != -1:

        title = tree.xpath(title_single_res_path)[0].split(' / ')[1]
        series_code = response_url.split('/watch/', 1)[1].split('-', 1)[0]

        print(f'{title} - {series_code}\n')

        print(f'Run this to download season 1 of {title}:')
        print(f'python main.py --sid={series_code} -s=1')
    else:

        elements = tree.xpath(element_xpath)

        for element in elements:

            title = element.xpath(english_title_xpath)[0].text

            # get series code from img src url
            series_code = element.xpath(code_xpath)[0].get('href').rsplit('/', 1)[1].split('-', 1)[0]

            print(f'{title} - {series_code}')


if __name__ == "__main__":

    term = ' '.join(sys.argv[1:])
    search(term)
