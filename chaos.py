import os
import string
import random
import time


string_tpl = string.ascii_lowercase + string.ascii_uppercase + string.digits


for _ in range(100):
    rand_str = ''.join(random.choice(string_tpl) for i in range(32))
    # print('Creating directory: "{}"'.format(rand_str))
    print(f'Creating directory: "{rand_str}"') # if python >= 3.6
    os.mkdir(rand_str)


delay = 5
print(f'All folders will be removed in {delay} seconds')
time.sleep(delay)


for name in os.listdir():
    if os.path.isdir(name):
        print(f'Directory detected: "{name}"\nRemoving...')
        os.rmdir(name)
    elif os.path.isfile(name):
        print(f'File name: "{name}"')
