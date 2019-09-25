from bs4 import BeautifulSoup
import requests
import datetime
from pprint import pprint


DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
BASE_URL = 'https://bash.im'
URL = f'{BASE_URL}/best'


doc = requests.get(URL)
soup = BeautifulSoup(doc.text, 'html.parser')


result = []
for i in soup.find_all('article', class_='quote'):
    post = i.find('a', href=True)
    raw_date = i.select_one('div.quote__header_date').text
    raw_date_list = raw_date.strip().split(' ')
    fixed_date = '{} {}'.format(raw_date_list[0], raw_date_list[-1])
    name = post.text
    rating = i.select_one('div.quote__total').text
    text = i.select_one('div.quote__body').text.strip()
    url = '{}{}'.format(BASE_URL, post['href'])
    timestamp = datetime.datetime.now().strftime(DATE_FORMAT)

    line = f'{name}, {rating}, {text}, {fixed_date}, {url}, {timestamp}'
    result.append(line)


print('\n\n'.join(result))
