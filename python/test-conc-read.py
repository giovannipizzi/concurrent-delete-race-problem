import os
import time
import sys

dest_fname = 'DEST.txt'

# Print only once
has_printed = False
for i in range(100000):
    try:
        print("BE", time.time())
        with open(dest_fname, 'rb') as fhandle:
            print("IN", time.time())
            content = fhandle.read()
            print("AF", time.time())
            try:
                assert content == b'CONTENT', 'FOUND INSTEAD: {}'.format(content)
            except AssertionError:
                print('ER1', fhandle.fileno(), os.fstat(fhandle.fileno()), file=sys.stderr)
                print('Exists:', os.path.exists(dest_fname), file=sys.stderr)
                raise
            else:
                if not has_printed:
                    print('OK-', fhandle.fileno(), os.fstat(fhandle.fileno()), file=sys.stderr)
                    has_printed = True
        print(i, content)
    except FileNotFoundError:
        print(i, ">> DELETED <<")
        # Recreate the file
        with open(dest_fname, 'wb') as fhandle:
            fhandle.write(b'CONTENT')

print("READ DONE.", file=sys.stderr)