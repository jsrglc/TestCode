from RedisDB import RedisClient
from GithubLogin import GithubLogin
import json

class CookiesGenerator():
    def __init__(self, website='default'):
        self.website = website
        self.cookies_db = RedisClient('cookies', self.website)
        self.accounts_db = RedisClient('accounts', self.website)
    
    def new_cookies(self, username, password):
        '''Get cookies, subclass needs to be overridden.'''
        raise NotImplementedError("new_cookies: not implemented!")

#    def process_cookies(self, cookies):
#        '''Handling cookies to dict style'''
#        dic = {}
#        for cookie in cookies:
#            dic[cookie['name']] = cookie['value']
#        return dic

    def run(self):
        '''check the cookies in redis'''
        accounts_usernames = self.accounts_db.usernames()
        cookies_usernames = self.cookies_db.usernames()
        for username in accounts_usernames:
            if not username in cookies_usernames:
                # if not exist, then generate
                password = self.accounts_db.get(username)
                print(' Generating Cookies', ' username: ', str(username,encoding='utf-8'), ' password: ', str(password, encoding='utf-8'))
                result = self.new_cookies(username, password)
                if result.get('status') == 1: # login succeeded
                     if self.cookies_db.set(username,json.dumps(result.get('content'))):
                        print('Save cookies successfully!')
                else:                         # login failed
                    print(result.get('content'))
                    if self.accounts_db.delete(username):
                        print('Account deleted successfully!')
    
class GithubCookiesGenerator(CookiesGenerator):
    def __init__(self, website='github'):
        CookiesGenerator.__init__(self, website)

    def new_cookies(self, username, password):
        '''Get cookies

        return:
            dict:{
                'status': status code, # 1: success, 0: fail
                'content': cookies
            }
        '''
        githublogin = GithubLogin()        
        return githublogin.login(username, password)

'''
if __name__ == "__main__":
    redis = RedisClient('accounts', 'github')
    redis.set('jsrglc', 'liuchennuaa2010')
    redis.set('js', 'liu')

    generator = GithubCookiesGenerator()
    generator.run() 
'''