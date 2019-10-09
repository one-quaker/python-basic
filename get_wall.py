import os
import random
import sys
import argparse
import time

from bs4 import BeautifulSoup
import requests


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
MODE_DOWN, MODE_RAND, MODE_ROTATE, MODE_ALL = ('download', 'random', 'rotate', 'all')
MODE_CHOICES = (MODE_DOWN, MODE_RAND, MODE_ROTATE, MODE_ALL)
DEFAULT_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:68.0) Gecko/20100101 Firefox/68.0'


parser = argparse.ArgumentParser()
parser.add_argument('-s', '--search', type=str, default='landscape')
parser.add_argument('-p', '--max-page', type=int, default=1)
parser.add_argument('-m', '--mode', type=str, choices=MODE_CHOICES, default=MODE_ALL)
parser.add_argument('-r', '--rotate-interval', type=int, default=600)
parser.add_argument('-O', '--out-dir', type=str, default='img')
parser.add_argument('-U', '--user-agent', type=str, default=DEFAULT_USER_AGENT)


ARG = parser.parse_args()


BASE_URL = 'https://www.pexels.com/search'
URL = '{}/{search}/'.format(BASE_URL, **ARG.__dict__)
IMG_ROOT_DIR = os.path.join(ROOT_DIR, ARG.out_dir)
IMG_DIR = os.path.join(IMG_ROOT_DIR, ARG.search)


USER_AGENT = ARG.user_agent


headers = {
    'user-agent': USER_AGENT,
}


for d in (IMG_ROOT_DIR, IMG_DIR):
    if not os.path.isdir(d):
        os.mkdir(d)


def download():
    for page in range(1, ARG.max_page + 1):
        if page == 1:
            page_url = URL
        else:
            page_url = f'{URL}?page={page}'
        print(f'Processing "{page_url}"')

        doc = requests.get(page_url, headers=headers)
        soup = BeautifulSoup(doc.text, 'html.parser')

        for i in soup.find_all('article', class_='photo-item'):
            img = i.find('img', class_='photo-item__img')
            url = img['src'].split('?')[0]

            fn = url.split('/')[-1]
            fp = os.path.join(IMG_DIR, fn)

            if not os.path.isfile(fp):
                print(f'Downloading "{url}"...')
                response = requests.get(url)

                with open(fp, 'wb') as f:
                    print(f'Saving to "{fp}"...')
                    f.write(response.content)


def apply_random_wallpaper():
    img_list = os.listdir(IMG_DIR)

    if not img_list:
        print(f'"{IMG_DIR}" is empty, skip...')
        return

    random_fn = random.choice(img_list)
    random_fp = os.path.join(IMG_DIR, random_fn)

    if sys.platform == 'darwin':
        os.system('osascript -e \'tell application "Finder" to set desktop picture to POSIX file "{}"\''.format(random_fp))
    elif sys.platform == 'win32':
        import struct
        import ctypes

        PATH = random_fp
        SPI_SETDESKWALLPAPER = 20

        def is_64bit_windows():
            """Check if 64 bit Windows OS"""
            return struct.calcsize('P') * 8 == 64

        def changeBG(path):
            """Change background depending on bit size"""
            if is_64bit_windows():
                ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 3)
            else:
                ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, path, 3)
        changeBG(PATH)

    else:
        print('Random image is not supported on your operating system "{}"'.format(sys.platform))


if ARG.mode == MODE_ALL:
    download()
    apply_random_wallpaper()
elif ARG.mode == MODE_DOWN:
    download()
elif ARG.mode == MODE_RAND:
    apply_random_wallpaper()
elif ARG.mode == MODE_ROTATE:
    while True:
        apply_random_wallpaper()
        time.sleep(ARG.rotate_interval)
