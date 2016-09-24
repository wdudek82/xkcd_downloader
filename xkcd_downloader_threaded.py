import logging
import os
import shutil
import threading

import requests
from bs4 import BeautifulSoup as Soup

logger = logging.getLogger('xkcd_downloader')
logger.setLevel(logging.INFO)
s_handler = logging.StreamHandler()
s_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s = %(levelname)s %(message)s')
s_handler.setFormatter(formatter)
logger.addHandler(s_handler)

try:
    shutil.rmtree('comics')
except FileNotFoundError as e:
    logger.warning('{} - creating one...'.format(e))
os.makedirs('comics', exist_ok=True)

def xkcd_downloader_threaded(start_comic, end_comic):
    logger = logging.getLogger('xkcd_downloader')
    logger.setLevel(logging.INFO)
    s_handler = logging.StreamHandler()
    s_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s = %(levelname)s %(message)s')
    s_handler.setFormatter(formatter)
    logger.addHandler(s_handler)

    root_url = 'http://xkcd.com/'

    counter = start_comic
    while counter < end_comic:
        url = '{}{}'.format(root_url, counter)
        response = requests.get(url)
        response.raise_for_status()

        soup = Soup(response.content, 'html.parser')


        try:
            img_url = soup.select('#comic img')[0].get('src')
            img_url = 'http:{}'.format(img_url)
        except IndexError as e:
            logger.warning('Finished! Position: {}'.format(counter))

        img = requests.get(img_url)
        img.raise_for_status()

        if img.status_code != 200:
            logger.warning('Counter: {}, status code was not 200 OK!'.format(counter))
            break

        logger.info('[{:03}] Downloading {} ...'.format(counter, img_url))

        file_name = '{}_{}'.format(counter, os.path.basename(img_url))
        file_path = os.path.join('comics', file_name)

        with open(file_path, 'wb') as img_file:
            logger.info('Saving image {} ...'.format(file_name))
            for img_chunk in img.iter_content(100000):
                img_file.write(img_chunk)

        counter += 1

for num in range(1, 2000, 100):
    thread = threading.Thread(target=xkcd_downloader_threaded, args=[num, num+99])
    thread.start()