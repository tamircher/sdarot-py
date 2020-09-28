import os
import time
from os.path import join

import requests
from bidi.algorithm import get_display
from colorama import init, Fore, Style
from lxml import html
from tqdm import tqdm

from configuration import Configuration
from utils import center

init(autoreset=True)


class SdarotPy:
    def __init__(self, sid, season_range=None, episode_range=None, output_path=Configuration.OUTPUT_PATH):

        if season_range is None:
            season_range = [1]
        if episode_range is None:
            episode_range = [1]

        self.sid = sid
        self.season = 1
        self.episode = 1

        self.output_path = os.path.abspath(output_path)

        self.season_range = season_range
        self.episode_range = episode_range

        # get serie name from the webpage
        self.serie_name = self.init_serie_name()

        self.url = f'{Configuration.SDAROT_MAIN_URL}/ajax/watch'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/60.0.3112.113 Safari/537.36',
            'Origin': f'{Configuration.SDAROT_MAIN_URL2}',
            'Referer': f'{Configuration.SDAROT_MAIN_URL2}/watch/',
        }
        self.s = requests.Session()
        self.s.headers.update(headers)

    def prepare_webpage_url(self):
        return f'{Configuration.SDAROT_MAIN_URL}/watch/{self.sid}/season/{self.season}/episode/{self.episode}'

    def init_serie_name(self):

        # get seire name
        res = requests.get(f'{Configuration.SDAROT_MAIN_URL2}/watch/{self.sid}')
        tree = html.fromstring(res.content)
        serie_name = ''.join(
            tree.xpath(
                '//div[@class="poster"]//h1//text()'
            )
        ).replace(' / ', '-')

        # remove invalid chars in folder name
        serie_name = serie_name.translate({ord(i): None for i in '/\\:*?"<>|'})
        return serie_name

    def get_data(self, url, data=None):

        if data is None:
            data = {}
        try:
            return self.s.post(url, data=data)
        except Exception as e:
            print(e)
        return None

    def get_video(self, video_url):

        # get video with stream
        res = self.s.get(video_url, stream=True)
        if not res or res.status_code != 200:
            print(Fore.RED + 'Error occurred, no video')
            return False

        # get the total file size
        file_size = int(res.headers.get("Content-Length", 0))

        # create directory for episode
        episode_path = join(
            self.output_path,
            f'{self.serie_name}',
            f'Season-{self.season}'
        )
        os.makedirs(episode_path, exist_ok=True)
        # get the file name
        filename = f'Episode-{self.episode}.mp4'

        # read 1024 bytes every time
        buffer_size = 1024
        # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
        progress = tqdm(
            iterable=res.iter_content(buffer_size),
            desc=Fore.CYAN + f"Downloading {filename}",
            total=file_size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        )

        with open(join(episode_path, filename), "wb") as f:
            for data in progress:
                # write data read to the file
                f.write(data)
                # update the progress bar manually
                if len(data) != 0:
                    progress.update(len(data))
        progress.close()

        return True

    def download_episode(self):

        # check if ep exsits
        temp_url = f'{Configuration.SDAROT_MAIN_URL}/watch/{self.sid}/season/{self.season}/episode/{self.episode}'
        res = requests.head(temp_url)
        if Configuration.DEBUG:
            print(f'Status: {res.status_code}')
        if res.status_code == 301:
            return False

        # pre watch
        data_prewatch = {
            'preWatch': 'true',
            'SID': self.sid,
            'season': self.season,
            'ep': self.episode
        }

        if Configuration.DEBUG:
            print('Getting Token...')
        res = self.get_data(self.url, data_prewatch)
        if not res or res.status_code != 200:
            print(Fore.RED + 'Error occurred, no token')
            return True

        token = res.content.decode("utf-8")
        if Configuration.DEBUG:
            print(f'Token: {token}')

        # 30 seconds loading
        print('Sleep 30 seconds for loading...')
        print(Fore.CYAN)
        for _ in tqdm(
                iterable=range(30),
                desc=Fore.BLUE + Style.BRIGHT + "Waiting"
        ):
            time.sleep(1)

        # watch

        data_watch = {
            'watch': 'true',
            'token': token,
            'serie': self.sid,
            'season': self.season,
            'episode': self.episode,
            'type': 'episode',
        }

        if Configuration.DEBUG:
            print('Getting Video URL...')
        res = self.get_data(self.url, data_watch)
        if not res or res.status_code != 200:
            print(Fore.RED + 'Error occurred, no json')
            return True

        try:
            content = res.json()
        except Exception as e:
            print(e)
            print(Fore.RED + 'Error occurred, no json')
            return True

        if "watch" not in content:
            print(Fore.RED + 'Busy servers, try again later')
            return False

        num = list(content["watch"].keys())[0]
        video_url = f'https:{content["watch"][num]}'
        if Configuration.DEBUG:
            print(f'Video URL: {video_url}')

        ret = self.get_video(video_url)
        if ret:
            print('Video downloaded successfully')
        else:
            print(Fore.RED + 'Video download failed')

        return True

    # download series with specified range
    def download_series(self):

        print(Fore.YELLOW + Style.BRIGHT + center(f'--==-- Serie: {get_display(self.serie_name)} --==--'))
        for self.season in self.season_range:
            print(Fore.GREEN + center(f'- - - - - [ Season: {self.season:02d} ] - - - - -'))

            for self.episode in self.episode_range:
                print(Fore.GREEN + Style.BRIGHT + center(f'---==={{ Episode: {self.episode:02d} }}===---'))

                # download episode to appropriate season inside
                if not self.download_episode():
                    break
