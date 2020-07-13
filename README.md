# concurrent-delete-race-problem
Debugging race problems when opening a file that is being deleted (on Mac OS)


## Notes
- There is a python version (go in `python` and run `./run-concurrent.sh`, that on Mac almost always raises the following error:

    ```
    OK- 3 os.stat_result(st_mode=33188, st_ino=8674943678, st_dev=16777220, st_nlink=0, st_uid=501, st_gid=20, st_size=7, st_atime=1594646008, st_mtime=1594646008, st_ctime=1594646008)
    ER1 3 os.stat_result(st_mode=32768, st_ino=0, st_dev=16777220, st_nlink=1, st_uid=0, st_gid=0, st_size=0, st_atime=0, st_mtime=0, st_ctime=0)
    Exists: False
    Traceback (most recent call last):
    File "test-conc-read.py", line 17, in <module>
        assert content == b'CONTENT', 'FOUND INSTEAD: {}'.format(content)
    AssertionError: FOUND INSTEAD: b''
    ```
    [Example of a run that failed like this](https://github.com/giovannipizzi/concurrent-delete-race-problem/runs/865343677?check_suite_focus=true#step:4:13)
    
    So it seems that when I get zero bytes, it's because `st_ino=0` (pointing to `inode` 0).

    Actually, very often I get the error:
    ```
    Traceback (most recent call last):
      File "test-conc-read.py", line 12, in <module>
        with open(dest_fname, 'rb') as fhandle:
    FileNotFoundError: [Errno 2] No such file or directory: 'DEST.txt'

    During handling of the above exception, another exception occurred:
    
    Traceback (most recent call last):
      File "test-conc-read.py", line 31, in <module>
        fhandle.write(b'CONTENT')
    OSError: [Errno 22] Invalid argument
    ```
    that is even another race condition that actually shows equally frequently.
    [Example of a run that failed like this](https://github.com/giovannipizzi/concurrent-delete-race-problem/runs/865319762?check_suite_focus=true#step:4:18)

- I managed to reproduce the problem **at least once** (but it's hard to reproduce in C)
  with the C code that seems to be doing the same.
  Note that on `C` the unlinks seem to be much faster, so I need to run for much longer I think.
  I got the output: 
  ```
  FOUND INSTEAD: ''
  ER ST_INO: 0
  ```
  [Example of a run that failed like this](https://github.com/giovannipizzi/concurrent-delete-race-problem/runs/865319777?check_suite_focus=true#step:4:9)

## Conclusions

In both cases, the error comes from the fact that the underlying `fopen` call returns an `fd`, but
this is associated with `st_ino` = 0.

