from bs4 import BeautifulSoup
import requests
import os
import random
import sys


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


BASE_URL = 'https://www.pexels.com/search'
URL = f'{BASE_URL}/landscape/'


doc = requests.get(URL)
soup = BeautifulSoup(doc.text, 'html.parser')


for i in soup.find_all('article', class_='photo-item'):
    img = i.find('img', class_='photo-item__img')
    url = img['src'].split('?')[0]

    fn = url.split('/')[-1]
    fp = os.path.join('img', fn)
    if not os.path.isfile(fp):
        print(f'Downloading "{url}"...')
        response = requests.get(url)

        with open(fp, 'wb') as f:
            print(f'Saving to "{fp}"...')
            f.write(response.content)


img_list = os.listdir('img')
fn = random.choice(img_list)
full_path = os.path.join(ROOT_DIR, 'img', fn)


if sys.platform == 'darwin':
    os.system('osascript -e \'tell application "Finder" to set desktop picture to POSIX file "{}"\''.format(full_path))
else:
    print('Random image is not supported on your operating system "{}"'.format(sys.platform))
