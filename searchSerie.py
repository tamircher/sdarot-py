import sys

import requests
from lxml import html

from configuration import Configuration

title_single_res_path = "//div[@class='poster']//h1/strong/text()"
element_xpath = "//div[contains(@class,'sInfo')]"
english_title_xpath = "./div/h5"
code_xpath = "./a"


def search(search_term):

    print(f'Searching for: {search_term}')
    # search term
    res = requests.get(f'{Configuration.SDAROT_MAIN_URL}/search?term={search_term}')
    tree = html.fromstring(res.content)

    response_url = res.url
    if response_url.find('/watch/') != -1:

        title = tree.xpath(title_single_res_path)[0].split(' / ')[1]
        serie_code = response_url.split('/watch/', 1)[1].split('-', 1)[0]

        print(f'{title} - {serie_code}\n')

        print(f'Run this to download season 1 of {title}:')
        print(f'python main.py --sid={serie_code} -s=1')
    else:

        elements = tree.xpath(element_xpath)

        for element in elements:

            title = element.xpath(english_title_xpath)[0].text

            # get serie code from img src url
            serie_code = element.xpath(code_xpath)[0].get('href').rsplit('/', 1)[1].split('-', 1)[0]

            print(f'{title} - {serie_code}')


if __name__ == "__main__":

    term = ' '.join(sys.argv[1:])
    search(term)
