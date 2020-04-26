from multiprocessing import Pool
from datetime import datetime
import time

def func(i):
    print('fun ', i ,' is started. ', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    time.sleep(i)
    print('fun ', i ,' is ended.   ', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

if __name__ == "__main__":
    pool = Pool(processes=3)
    for i in range(2, 6):
        pool.apply(func, (i,))
#    pool.map(func, [i for i in range(2, 6)])
    print('back of map ...')
    pool.close()
    print('back of close ...')
    pool.join()
    print('end of main ...')