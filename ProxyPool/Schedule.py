#from multiprocessing import Pool as ThreadPool
from FlaskServer import app
from Getter import Getter
from Tester import tester_run
import time

TESTER_CYCLE = 2000
GETTER_CYCLE = 2000
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

class Scheduler():
    def scheduler_tester(self, cycle=TESTER_CYCLE):
        '''
        Run tester
        '''
        print(' Tester is running ...')
        tester_run()
#        while True:
#            print(' Tester is running ...')
#            tester_run()
#            time.sleep(cycle)
            
    def scheduler_getter(self, cycle=GETTER_CYCLE):
        '''
        Run getter
        '''
        print(' Getter is running ...')
        getter = Getter()
        getter.run()
#        while True:
#            print(' Getter is running ...')
#            getter.run()
#            time.sleep(cycle)

    def scheduler_api(self):
        '''
        Run api
        '''
        print(' Api is running ...')
        app.run()
    
    def run(self):
        '''
        Starting proxypool
        '''
        print(' starting ProxyPool ...')
        self.scheduler_getter()
        self.scheduler_tester()
#        self.scheduler_api() 
#        pool = ThreadPool()
#        if GETTER_ENABLED:
#            pool.apply_async(self.scheduler_getter)
#        if TESTER_ENABLED:
#            pool.apply_async(self.scheduler_tester)
#        if API_ENABLED:
#            pool.apply_async(self.scheduler_api)
#        pool.close()
#        pool.join()
    
if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.run()