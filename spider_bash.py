from bs4 import BeautifulSoup
import requests
from pprint import pprint
import datetime
import json
import random
import time


BASE_URL = 'https://bash.im'
URL = f'{BASE_URL}/best'
# URL = '{}/best'.format(BASE_URL)
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:68.0) Gecko/20100101 Firefox/68.0'


headers = {
    'user-agent': USER_AGENT,
}


doc = requests.get(URL, headers=headers)
soup = BeautifulSoup(doc.text, 'html.parser')
# print(doc.text)


result = [] # list

for i in soup.find_all('article', class_='quote'):
    delay = random.randint(30, 50) / 10
    time.sleep(delay)
    print(f'sleep for "{delay}" seconds...')

    post = i.find('a', class_='quote__header_permalink')
    text = i.find('div', class_='quote__body').text.strip()
    raw_rating = i.find('div', class_='quote__total').text.strip()

    try:
        rating = int(raw_rating)
    except ValueError:
        rating = 0

    ts = i.find('div', class_='quote__header_date').text.strip()
    # print(32 * '-')
    url = '{}{}'.format(BASE_URL, post['href'])
    # url = '{0}{1}'.format(BASE_URL, post['href'])
    # print(url)
    # print(rating)
    # print(text)
    post_date, post_time = ts.split(' в ')
    # print(post_date, post_time)
    final_ts = '{} {}'.format(post_date.strip(), post_time.strip())
    final_dt = datetime.datetime.strptime(final_ts, '%d.%m.%Y %H:%M')
    new_dt = final_dt.strftime('%Y.%m.%d')
    # print(final_ts)
    # print(final_dt)
    # print(new_dt)
    # post_item = [url, rating, text, final_ts]
    post_item = (url, rating, text, final_ts)
    result.append(post_item)


pprint(result)


# with open('bash.txt', 'w') as f:
#     for i in result:
#         line = '\n'.join(i)
#         f.write('\n------\n' + line)

with open('bash.json', 'w') as f:
    # json.dump(result, f, indent=4, separators=(',', ': '), sort_keys=True)
    json.dump(result, f, indent=4, ensure_ascii=False) # maybe fail in windows
    # json.dump(result, f, indent=4)


with open('bash.json') as f:
    from_json = json.load(f)
    print(32 * '-')
    print(from_json)
