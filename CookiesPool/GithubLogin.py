import requests
from pyquery import PyQuery as pq

class GithubLogin():
    def __init__(self):
        self.headers = {
            'Referer': 'https://github.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'host': 'github.com'
        }
        self.login_url = 'https://github.com/login'
        self.post_url = 'https://github.com/session'
        self.session = requests.Session()

    def token(self):
        response = self.session.get(url=self.login_url, headers=self.headers)
        doc = pq(response.text)
        token = doc('#login > form > input:first').attr('value')
        return token
    
    def login(self, name, password):
        post_data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': self.token(),
            'login': name,
            'password': password
        }

        response = self.session.post(url=self.post_url, data=post_data, headers=self.headers)
        if response.status_code == 200:
            doc = pq(response.text)
            if not doc('#js-flash-container > div[class*=flash-error]'):
                cookies = requests.utils.dict_from_cookiejar(response.cookies)
                return {
                    'status': 1,
                    'content': cookies
                }
            else:
                return {
                    'status': 0,
                    'content': 'Username or password wrong.'
                }
        else:
            return {
                'status': response.status_code,
                'content': 'Request could not be completed.'
            }

'''
if __name__ == "__main__":
    githublogin = GithubLogin()
    result = githublogin.login(name='js', password='liuc')

    print(result.get('status'))
    print(type(result.get('content')))
    print(len(result.get('content')))
    print(result.get('content'))
'''