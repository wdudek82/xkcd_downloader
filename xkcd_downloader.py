import os
import logging
import shutil

import requests
from bs4 import BeautifulSoup as Soup


logger = logging.getLogger('xkcd_downloader')
logger.setLevel(logging.INFO)
s_handler = logging.StreamHandler()
s_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s = %(levelname)s %(message)s')
s_handler.setFormatter(formatter)
logger.addHandler(s_handler)

root_url = 'http://xkcd.com/'

try:
    shutil.rmtree('comics')
except FileNotFoundError as e:
    logger.warning('{} - creating one...'.format(e))

os.makedirs('comics', exist_ok=True)

counter = 1
while 1:
    url = '{}{}'.format(root_url, counter)
    response = requests.get(url)

    soup = Soup(response.content, 'html.parser')


    try:
        img_url = requests.utils.quote(soup.find_all('img')[1].get('src'))
        img_url = 'http:{}'.format(img_url)
    except IndexError as e:
        logger.warning('Finished! Position: {}'.format(counter))

    img = requests.get(img_url)
    if img.status_code != 200:
        logger.warning('Counter: {}, status code was not 200 OK!'.format(counter))
        break

    logger.info('[{:03}] Downloading {} ...'.format(counter, img_url))

    file_name = '{}_{}'.format(counter, os.path.basename(img_url))
    file_path = os.path.join('comics', file_name)

    with open(file_path, 'wb') as img_file:
        logger.info('Saving image {} ...'.format(file_name))
        img_file.write(img.content)

    counter += 1