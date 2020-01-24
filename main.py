from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

# URL of sdarot
URL = 'https://sdarot.today/watch'
# name of series
SERIES = '3199-אפל-dark'

# end target to get the video from
TARGET = f'{URL}/{SERIES}/season/1/episode/1'

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 31)


browser.get(TARGET)

try:
  buttonElement = browser.find_element_by_id("proceed")

  # wait for video to load (30 seconds)
  video = wait.until(EC.presence_of_element_located((By.ID, "videojs_html5_api")))

  # get video url
  video_url = video.get_property('src')

  # copy cookies to request
  cookies = browser.get_cookies()
  s = requests.Session()
  for cookie in cookies:
      s.cookies.set(cookie['name'], cookie['value'])

  # get video with stream
  response = s.get(video_url, stream=True)
  print(response.status_code)

  # save video file (takes time, progress not visible)
  with open('temp_name.mp4','wb') as f:
      f.write(response.content)
  
finally:
  browser.quit()
  

