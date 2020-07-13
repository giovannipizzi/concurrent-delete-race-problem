import os
import sys
import time

dest_fname = 'DEST.txt'
for i in range(100000):
    if os.path.exists(dest_fname):
        print("BE", time.time())
        os.unlink(dest_fname)
        print("AF", time.time())
        print(dest_fname, i, 'DELETED')
    else:
        print(dest_fname, i, 'continue')

print("DELETE DONE.", file=sys.stderr)