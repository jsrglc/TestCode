from RedisDB import RedisClient

class Random_Proxy():
    def __init__(self):
        self.db = RedisClient()

    def get_proxy(self):
        '''
        Get a random proxy
        '''
        return str(self.db.random(), encoding='utf-8')