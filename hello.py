import sys


if sys.platform == 'linux':
    print('Hello Linux!')
elif sys.platform == 'darwin':
    print('Hello Mac!')
elif sys.platform == 'win32':
    print('Hello Windows!')
else:
    print('Hello Unknown OS!')
