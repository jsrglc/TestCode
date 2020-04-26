from flask import Flask, g
from RedisDB import RedisClient

app = Flask(__name__)

def get_conn():
    '''
    Get redis client object
    '''
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis

@app.route('/')
def index():
    '''
    Get home page, you can define your own templates
    '''
    return '<h2>Welcome to Proxy Pool System</h2>'

@app.route('/random')
def get_proxy():
    '''
    Get a random proxy
    '''
    conn = get_conn()
    return conn.random()

@app.route('/count')
def get_counts():
    '''
    Get the count fo proxies
    '''
    conn = get_conn()
    return str(conn.count())