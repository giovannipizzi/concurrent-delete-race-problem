import os
import psutil
import time

dest_fname = 'DEST.txt'
for i in range(100000):
    try:
        print("BE", time.time())
        fhandle = open(dest_fname, 'rb')
        print("IN", time.time())
        content = fhandle.read()
        print("AF", time.time())
        assert content == b'CONTENT', 'FOUND INSTEAD: {}'.format(content)
        fhandle.close()
        print(i, content)
    except FileNotFoundError:
        print(i, ">> DELETED <<")
        # Recreate the file
        with open(dest_fname, 'wb') as fhandle:
            fhandle.write(b'CONTENT')
