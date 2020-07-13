import numpy as np
import pylab as plt
from tqdm import tqdm

WINDOW_SIZE_SEC_PRE = 0.01
WINDOW_SIZE_SEC_POST = 0.01

with open('read.txt') as f:
    read_data = f.readlines()
read_data = [line.strip() for line in read_data if line.startswith('BE ') or line.startswith('IN ') or line.startswith('AF ')]

with open('del.txt') as f:
    del_data = f.readlines()
del_data = [line.strip() for line in del_data if line.startswith('BE ') or line.startswith('AF ')]

read_pre_ranges = []
read_post_ranges = []
current = []
last = None
for line in read_data:
    try:
        when, time = line.split()
    except Exception:
        print(line)
        raise
    if when == 'BE':
        if last == 'BE':
            # TODO: have it print something even if the file is deleted
            continue
        assert (last is None) or (last == 'AF'), f'last={last}'
        assert not current
        current.append(float(time))
    elif when == 'IN':
        assert len(current) == 1
        assert last == 'BE'
        current.append(float(time))
        read_pre_ranges.append(current)
        current = [float(time)]
    elif when == 'AF':
        assert last == 'IN'
        assert len(current) == 1
        current.append(float(time))
        read_post_ranges.append(current)
        current = []
    else:
        raise ValueError(f'unknown prefix {when}')
    last = when
#assert not current

ref_time = read_pre_ranges[-1][1] #- 2
min_time = ref_time - WINDOW_SIZE_SEC_PRE
max_time = ref_time + WINDOW_SIZE_SEC_POST

read_pre_ranges = [read_range for read_range in read_pre_ranges if read_range[1] > min_time and read_range[1] < max_time]
read_post_ranges = [read_range for read_range in read_post_ranges if read_range[1] > min_time and read_range[1] < max_time]

del_ranges = []
current = []
for line in del_data:
    try:
        when, time = line.split()
    except Exception:
        print(line)
        raise
    if when == 'BE':
        assert not current
        current.append(float(time))
    elif when == 'AF':
        assert len(current) == 1
        current.append(float(time))
        if float(time) > min_time and float(time) < max_time:
            del_ranges.append(current)
        current = []
    else:
        raise ValueError(f'unknown prefix {when}')
assert not current

print("Deletions")
for idx, del_range in enumerate(tqdm(del_ranges)):
    plt.plot(np.array(del_range) - ref_time, [0, 0], '-', color='red', linewidth=1, label=None if idx else 'deletions')

print("Read-pre")
for idx, read_range in enumerate(tqdm(read_pre_ranges)):
    plt.plot(np.array(read_range) - ref_time, [0.2, 0.25], 'g-', linewidth=1, label=None if idx else 'read (open)')

print("Read-post")
for idx, read_range in enumerate(tqdm(read_post_ranges)):
    plt.plot(np.array(read_range) - ref_time, [0.25, 0.2], 'k-', linewidth=1, label=None if idx else 'read (read)')

plt.legend(loc='best')
plt.show()
