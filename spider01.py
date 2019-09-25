from bs4 import BeautifulSoup
import requests
import datetime
from pprint import pprint


DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
BASE_URL = 'https://bash.im'
URL = f'{BASE_URL}/best'


doc = requests.get(URL)
soup = BeautifulSoup(doc.text, 'html.parser')


def write_json(data, fp):
    import json
    with open(fp, 'w') as f:
        json.dump(data, f, indent=4, separators=(',', ': '), sort_keys=True)


result = []
for i in soup.find_all('article', class_='quote'):
    item = {}

    print(16 * '-')
    # print(i.text)

    post = i.find('a', href=True)
    raw_date = i.select_one('div.quote__header_date').text
    # print(raw_date)
    raw_date_list = raw_date.strip().split(' ')
    # print(raw_date_list)
    fixed_date = '{} {}'.format(raw_date_list[0], raw_date_list[-1])
    # print(fixed_date)

    item['name'] = post.text

    try:
        rating = int(i.select_one('div.quote__total').text)
    except ValueError:
        rating = 0
        print('Invalid digit in text "{}"'.format(post.text))

    item['rating'] = rating
    item['text'] = i.select_one('div.quote__body').text.strip()
    item['date'] = fixed_date
    # item['text'] = i.find('div', class_='quote__body').text
    item['url'] = '{}{}'.format(BASE_URL, post['href'])
    item['date_format'] = DATE_FORMAT
    item['timestamp'] = datetime.datetime.now().strftime(DATE_FORMAT)
    result.append(item)


pprint(result)
write_json(result, 'result.json')
