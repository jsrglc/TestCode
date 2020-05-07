from RedisDB import RedisClient
import json, requests

class ValidTester():
    def __init__(self, website='default'):
        self.website = website
        self.cookies_db = RedisClient('cookies', self.website)
        self.accounts_db = RedisClient('accounts', self.website)
    
    def test(self, username, cookies):
        raise NotImplementedError('test: not implemented!')

    def run(self):
        cookies_groups = self.cookies_db.all()
        for username, cookies in cookies_groups.items():
            self.test(username, cookies)

class GithubValidTester(ValidTester):
    def __init__(self, website='github'):
        ValidTester.__init__(self, website)

    def test(self, username, cookies):
        print(' Testing Cookies, username: ', username)
        try:
            cookies = json.loads(cookies)
        except TypeError:
            print(' Cookies illegal: ', username)
            self.cookies_db.delete(username)
            print(' Delete Cookies: ', username)
            return
        try:
            test_url = 'https://github.com/'            
            headers = {
                'Referer': 'https://github.com/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
                'host': 'github.com'
            }
            response = requests.get(test_url, headers=headers, cookies=cookies, timeout=5)
            if response.status_code  == 200:
                print(' Cookies is useful. username: ', username)
                print(' Partial result of testing: ', response.text[:100])
            else:
                print(response.status_code, response.headers)
                print(' Cookies is unuseful. username: ', username)
                self.cookies_db.delete(username)
                print(' Delete Cookies: ', username)
        except ConnectionError as e:
            print(' Error: ', e.args)

#if __name__ == "__main__":
#    test = GithubValidTester()
#    test.run()