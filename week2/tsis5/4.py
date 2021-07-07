import sys
import os
def file_read_from_tail(file_name, n):
        bufsize, iter = 8192, 0
        fsize = os.stat(fname).st_size
        with open(file_name) as f:
                if bufsize > fsize:
                        bufsize = fsize-1
                        data = []
                        while True:
                                iter +=1
                                f.seek(fsize-bufsize*iter)
                                data.extend(f.readlines())
                                if len(data) >= lines or f.tell() == 0:
                                        print(''.join(data[-n:]))
                                        break

file_read_from_tail('test.txt', int(input()))