import os
import time
from os.path import join
import random
import requests
from bidi.algorithm import get_display
from colorama import init, Fore, Style
from lxml import html
from tqdm import tqdm

from configuration import Configuration
from utils import center, ErrorCodes

init(autoreset=True)


class SdarotPy:
    def __init__(self, sid, season_range=None, episode_range=None, output_path=Configuration.OUTPUT_PATH):

        self.sid = sid

        # get series name from the webpage
        series_info = self.get_series_info()
        self.series_name = series_info['name']
        if season_range is None:
            season_range = series_info['seasons']

        if episode_range is None:
            episode_range = [1]

        print(center(
            Fore.YELLOW +
            f'----====[ Fetching: Seasons {season_range[0]}-{season_range[-1]}, Episodes {episode_range[0]}-{episode_range[-1]} ]====----'))

        self.season = 1
        self.episode = 1

        self.output_path = os.path.abspath(output_path)

        self.season_range = season_range
        self.episode_range = episode_range

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

    def get_series_info(self):

        # get series name
        res = requests.get(f'{Configuration.SDAROT_MAIN_URL2}/watch/{self.sid}')
        tree = html.fromstring(res.content)
        series_name = ''.join(
            tree.xpath(
                '//div[@class="poster"]//h1//text()'
            )
        ).replace(' / ', ' - ')

        # remove invalid chars in folder name
        series_name = series_name.translate({ord(i): None for i in '/\\:*?"<>|'})

        season_numbers = tree.xpath('//ul[@id="season"]//li["data-season"]')
        season_numbers = list(map(lambda el: int(el.attrib.get('data-season')), season_numbers))

        return {
            'name': series_name,
            'seasons': season_numbers,
        }

    def get_data(self, url, data=None):

        if data is None:
            data = {}
        try:
            return self.s.post(url, data=data)
        except Exception as e:
            print(e)
        return None

    def get_video(self, video_url):
        download_exist = False
        file_size_offline = 0

        # create directory for episode
        episode_path = join(self.output_path,
                            f'{self.series_name}',
                            f'Season-{self.season:02d}')
        os.makedirs(episode_path, exist_ok=True)

        # get the file name
        filename = f'Episode-{self.episode:02d}.mp4'
        offline_filename = join(episode_path, filename)

        # if file exists set Range header to start stream from the file size
        if os.path.isfile(offline_filename):
            download_exist = True
            file_size_offline = os.stat(offline_filename).st_size
            print(f'Found existing episode: {filename}.')

        self.s.headers.update({'Range': f'bytes={file_size_offline}-'})

        # get video with stream
        res = self.s.get(video_url, stream=True)
        if not res and res.status_code not in (200, 206, 416):
            print(Fore.RED + f'Error occurred, no video. ( HTTP ERROR: {res.status_code} )')
            return {'isOk': False, 'errors': ErrorCodes.UNKNOWN_ERROR}

        if res.status_code == 416:
            print('Episode already downloaded - skipping download')
            return {'isOk': True, 'errors': None}

        # get the total file size
        file_size_online = int(res.headers.get("Content-Range").split('/')[1])

        print('Downloading....' if not download_exist else 'Resuming download....')

        # Set configuration
        buffer_size = 1024
        mode = 'ab' if download_exist else 'wb'

        # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
        progress = tqdm(
            iterable=res.iter_content(buffer_size),
            desc=Fore.CYAN + f"Downloading {filename}",
            total=file_size_online,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            initial=file_size_offline,
            leave=False
        )
        with open(offline_filename, mode) as f:
            for data in progress:
                # write data read to the file
                f.write(data)
                # update the progress bar manually
                if len(data) != 0:
                    progress.update(len(data))
        progress.close()

        print('Video downloaded successfully')
        return {'isOk': True, 'errors': None}

    def is_page_exists(self, url):
        res = requests.head(url)
        if Configuration.DEBUG:
            print(f'Status: {res.status_code}')
        if res.status_code == 301:
            return False
        return True

    def download_episode(self):

        # pre watch
        data_pre_watch = {
            'preWatch': 'true',
            'SID': self.sid,
            'season': self.season,
            'ep': self.episode
        }

        if Configuration.DEBUG:
            print('Getting Token...')
        res = self.get_data(self.url, data_pre_watch)
        if not res or res.status_code != 200:
            print(Fore.RED + 'Error occurred, no token')
            return {'isOk': False, 'errors': ErrorCodes.NO_TOKEN}

        token = res.content.decode("utf-8")
        if Configuration.DEBUG:
            print(f'Token: {token}')

        # 30 seconds loading
        print('Waiting 30 seconds before download...')
        print(Fore.CYAN)
        for _ in tqdm(
                iterable=range(30),
                desc=Fore.BLUE + Style.BRIGHT + "Waiting",
                leave=False
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
            return {'isOk': False, 'errors': ErrorCodes.NO_JSON}

        try:
            content = res.json()
        except Exception as e:
            print(e)
            print(Fore.RED + 'Error occurred, no json')
            return {'isOk': False, 'errors': ErrorCodes.NO_TOKEN}

        if "watch" not in content:
            print(Fore.RED + 'Busy servers, try again later')
            return {'isOk': False, 'errors': ErrorCodes.SERVER_BUSY}

        num = list(content["watch"].keys())[0]
        video_url = f'https:{content["watch"][num]}'
        if Configuration.DEBUG:
            print(f'Video URL: {video_url}')

        ret = self.get_video(video_url)
        if not ret['isOk']:
            print(Fore.RED + 'Video download failed')

        return {'isOk': True, 'errors': None}

    # download series with specified range
    def download_series(self):

        print(Fore.YELLOW + Style.BRIGHT + center(f'--==-- Series: {get_display(self.series_name)} --==--'))
        for self.season in self.season_range:

            # check if season exists
            season_url = f'{Configuration.SDAROT_MAIN_URL}/watch/{self.sid}/season/{self.season}/episode/1'
            if not self.is_page_exists(season_url):
                continue

            print(Fore.GREEN + center(f'- - - - - [ Season: {self.season:02d} ] - - - - -'))

            for self.episode in self.episode_range:

                # check if ep exists
                temp_url = f'{Configuration.SDAROT_MAIN_URL}/watch/{self.sid}/season/{self.season}/episode/{self.episode}'
                if not self.is_page_exists(temp_url):
                    break  # continue to next season

                print(Fore.GREEN + Style.BRIGHT + center(f'---==={{ Episode: {self.episode:02d} }}===---'))
                episode_download_retry_counter = 0
                while True:
                    # download episode to appropriate season inside
                    download_result = self.download_episode()
                    if download_result['isOk'] or episode_download_retry_counter >= Configuration.MAX_RETRY_ON_BUSY:
                        break
                    else:
                        if download_result['errors'] == ErrorCodes.SERVER_BUSY:
                            episode_download_retry_counter = episode_download_retry_counter + 1
                            print(
                                f'Retrying to download episode [{episode_download_retry_counter}/{Configuration.MAX_RETRY_ON_BUSY}]')
                            busy_wait_time = random.randint(Configuration.MIN_RETRY_TIME, Configuration.MAX_RETRY_TIME)
                            # 30 seconds loading
                            print(f'Waiting {busy_wait_time} seconds before trying again to download...')
                            print(Fore.CYAN)
                            for _ in tqdm(
                                    iterable=range(busy_wait_time),
                                    desc=Fore.BLUE + Style.BRIGHT + "Waiting",
                                    leave=False
                            ):
                                time.sleep(1)
                        else:
                            break
