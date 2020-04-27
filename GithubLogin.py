import requests
from pyquery import PyQuery as pq

class Login():
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
            self.repositories(response.text)

    def repositories(self, html):
        doc = pq(html)

        name = doc('.header-nav-current-user.css-truncate > a > strong').text().strip()
        print('name: ', name)

        print('respositories:')
        items = doc('.news #repos-container > ul > li').items()
        for item in items:
            repository = item.text().strip()
            print(repository)

if __name__ == "__main__":
    login = Login()
    login.login(name='jsrglc', password='liuchennuaa2010')