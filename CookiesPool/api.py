import json
from flask import Flask, g
from RedisDB import RedisClient

app = Flask(__name__)

@app.route('/')
def index():
    return '<h2>Welcome to Cookie Pool System!</h2>'

def get_conn():
    website='github'
    if not hasattr(g, website):
        setattr(g, website + '_cookies', eval('RedisClient' + '("cookies", "' + website + '")'))
        return g

@app.route('/github/random')
def random():
    g = get_conn()
    cookies = getattr(g, 'github_cookies').random()
    return cookies

#if __name__ == "__main__":
#    app.run()