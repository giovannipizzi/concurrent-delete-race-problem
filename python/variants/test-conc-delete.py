import os
import psutil
import uuid
import time

TRASH = 'trash'
try:
    os.mkdir(TRASH)
except FileExistsError:
    pass

def my_remove(path):
    trash_path = os.path.join(TRASH, '{}-{}'.format(os.path.basename(path), str(uuid.uuid4())))
    os.rename(path, trash_path)
    print("BE", time.time())
    os.remove(trash_path)
    print("AF", time.time())

dest_fname = 'DEST.txt'
for i in range(100000):
    if os.path.exists(dest_fname):
        my_remove(dest_fname)
        #os.unlink(dest_fname)
        print(dest_fname, i, 'DELETED')
    else:
        print(dest_fname, i, 'continue')
