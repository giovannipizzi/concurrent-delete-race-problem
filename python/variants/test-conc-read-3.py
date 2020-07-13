import os
import psutil
import time

dest_fname = 'DEST.txt'
for i in range(100000):
    try:
        print("BE", time.time())
        fd = os.open(dest_fname, os.O_RDONLY) #  | os.O_BINARY exists only on windows
        print("IN", time.time())
        content = os.read(fd, 100) # Read enough bytes
        print("AF", time.time())
        assert content == b'CONTENT', 'FOUND INSTEAD: {}'.format(content)
        os.close(fd)
        print(i, content)
    except FileNotFoundError:
        print(i, ">> DELETED <<")
        # Recreate the file
        with open(dest_fname, 'wb') as fhandle:
            fhandle.write(b'CONTENT')
