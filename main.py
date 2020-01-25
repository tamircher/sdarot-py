import requests
import time
from tqdm import tqdm

sid = 5174
season = 1
episode = 1


# URL of sdarot
url = 'https://sdarot.today/ajax/watch'
# name of series
OPTIONS = {'SID': sid, 'season': season, 'ep': episode}


data_prewatch = {'preWatch': 'true', **OPTIONS}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Origin': 'http://sdarot.today',
    'Referer': 'http://sdarot.today/watch/',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
}


s = requests.Session()
s.headers.update(headers)

print('Getting Token...')
res = s.post(url, data=data_prewatch)
if res.status_code != 200:
    print('Error occured, no token')
    exit()

token = res.content.decode("utf-8")
print(f'Token: {token}')


print('Sleep 30 seconds for loading...')
for i in tqdm(range(30)):
    time.sleep(1)


data_watch = {
    'watch': 'true',
    'token': token,
    'serie': OPTIONS["SID"],
    'season': OPTIONS["season"],
    'episode': OPTIONS["ep"],
    'type': 'episode',
}

print('Getting Video URL...')
res = s.post(url, data=data_watch)
if res.status_code != 200:
    print('Error occured, no json')
    exit()

content = res.json()
num = list(content['watch'].keys())[0]
video_url = f'https://{content["url"]}/w/episode/{num}/{content["VID"]}.mp4?token={content["watch"][num]}&time={content["time"]}'
print(f'Video URL: {video_url}')


# get video with stream
res = s.get(video_url, stream=True)
print(res.status_code)

# get the total file size
file_size = int(res.headers.get("Content-Length", 0))
# get the file name
filename = f'{content["eng"]}-s{season}-e{episode}.mp4'

# read 1024 bytes every time
buffer_size = 1024
# progress bar, changing the unit to bytes instead of iteration (default by tqdm)
progress = tqdm(res.iter_content(buffer_size),
                f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    for data in progress:
        # write data read to the file
        f.write(data)
        # update the progress bar manually
        if(len(data) != 0):
            progress.update(len(data))
progress.close()
