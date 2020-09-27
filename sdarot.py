import requests
import time
import os
from tqdm import tqdm
from os.path import join
from lxml import html


class SdarotPy:
    def __init__(self, sid, season_range=[1], episode_range=[1], output_path='output'):

        self.sid = sid
        self.season = 1
        self.episode = 1

        self.output_path = os.path.abspath(output_path)

        self.season_range = season_range
        self.episode_range = episode_range

        # get serie name from the webpage
        self.serie_name = self.init_serie_name()

        self.url = 'https://sdarot.today/ajax/watch'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Origin': 'http://sdarot.today',
            'Referer': 'http://sdarot.today/watch/',
        }
        self.s = requests.Session()
        self.s.headers.update(headers)

    def prepare_webpage_url(self):
        return f'https://sdarot.today/watch/{self.sid}/season/{self.season}/episode/{self.episode}'

    def init_serie_name(self):

        ### get seire name ###
        res = requests.get(f'http://sdarot.today/watch/{self.sid}')
        tree = html.fromstring(res.content)
        serie_name = ''.join(tree.xpath(
            '//div[@class="poster"]//h1//text()')).replace(' / ', '-')

        # remove invalid chars in folder name
        serie_name = serie_name.translate({ord(i): None for i in '/\:*?"<>|'})
        return serie_name

    def get_data(self, url, data={}):

        try:
            return self.s.post(url, data=data)
        except Exception as e:
            print(e)
        return None

    def get_video(self, video_url):

        # get video with stream
        res = self.s.get(video_url, stream=True)
        if not res or res.status_code != 200:
            print('Error occured, no video')
            return False

        # get the total file size
        file_size = int(res.headers.get("Content-Length", 0))

        # create direcotory for episode
        episode_path = join(self.output_path, f'{self.serie_name}',
                            f'Season-{self.season}')
        os.makedirs(episode_path, exist_ok=True)
        # get the file name
        filename = f'Episode-{self.episode:02d}.mp4'

        # read 1024 bytes every time
        buffer_size = 1024
        # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
        progress = tqdm(res.iter_content(buffer_size),
                        f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
        with open(join(episode_path, filename), "wb") as f:
            for data in progress:
                # write data read to the file
                f.write(data)
                # update the progress bar manually
                if(len(data) != 0):
                    progress.update(len(data))
        progress.close()

        return True

    def download_episode(self):

        ### check if ep exsits ###
        temp_url = f'https://sdarot.today/watch/{self.sid}/season/{self.season}/episode/{self.episode}'
        res = requests.head(temp_url)
        print(f'Status: {res.status_code}')
        if res.status_code == 301:
            return False

        ### pre watch ###

        data_prewatch = {
            'preWatch': 'true',
            'SID': self.sid,
            'season': self.season,
            'ep': self.episode
        }

        print('Getting Token...')
        res = self.get_data(self.url, data_prewatch)
        if not res or res.status_code != 200:
            print('Error occured, no token')
            return True

        token = res.content.decode("utf-8")
        print(f'Token: {token}')

        ### 30 seconds loading ###

        print('Sleep 30 seconds for loading...')
        for _ in tqdm(range(30)):
            time.sleep(1)

        ### watch ##

        data_watch = {
            'watch': 'true',
            'token': token,
            'serie': self.sid,
            'season': self.season,
            'episode': self.episode,
            'type': 'episode',
        }

        print('Getting Video URL...')
        res = self.get_data(self.url, data_watch)
        if not res or res.status_code != 200:
            print('Error occured, no json')
            return True

        try:
            content = res.json()
        except Exception as e:
            print(e)
            print('Error occured, no json')
            return True

        if "watch" not in content:
            print('Busy servers, try again later')
            return False

        num = list(content["watch"].keys())[0]
        video_url = f'https:{content["watch"][num]}'
        print(f'Video URL: {video_url}')

        ret = self.get_video(video_url)
        if ret:
            print('Video downloaded successfully')
        else:
            print('Video download failed')

        return True

    # donwload series with specified range
    def download_series(self):

        for self.season in self.season_range:
            print(f'\n--------Season {self.season}---------\n')

            for self.episode in self.episode_range:
                print(f'\n  ------Episode {self.episode}------\n')

                # download episode to appropriate season inside
                if not self.download_episode():
                    break
