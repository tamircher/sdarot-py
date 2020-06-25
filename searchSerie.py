import requests
from lxml import html
import sys


element_xpath = "//div[contains(@class,'sInfo')]"
english_title_xpath = "./div/h5"
code_xpath = "./a"

term = sys.argv[1]
### search term ###
res = requests.get(f'https://sdarot.today/search?term={term}')
tree = html.fromstring(res.content)
elements = tree.xpath(element_xpath)

for element in elements:

    title = element.xpath(english_title_xpath)[0].text

    # get serie code from img src url
    serie_code = element.xpath(code_xpath)[0].get(
        'href').rsplit('/', 1)[1].split('-', 1)[0]

    print(f'{title} - {serie_code}')
