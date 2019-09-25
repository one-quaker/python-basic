from bs4 import BeautifulSoup
import requests
from pprint import pprint


BASE_URL = 'https://bash.im'
URL = f'{BASE_URL}/best'


doc = requests.get(URL)
soup = BeautifulSoup(doc.text, 'html.parser')


result = [] # list

for i in soup.find_all('article', class_='quote'):
    post = i.find('a', href=True)
    text = i.select_one('div.quote__body').text.strip()
    url = '{}{}'.format(BASE_URL, post['href'])
    raw_date = i.select_one('div.quote__header_date').text
    # raw_date_list = raw_date.strip().split(' ')
    # fixed_date = '{} {}'.format(raw_date_list[0], raw_date_list[-1])
    name = post.text
    rating = i.select_one('div.quote__total').text

    line = f'Name: {name}\nUrl: {url}\nRating: {rating}\n\n{text}\n-------'
    result.append(line)


with open('result.txt', 'w') as f:
    f.write('\n\n'.join(result))
