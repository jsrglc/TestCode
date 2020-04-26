import requests, time
from FlaskServer import app
from multiprocessing import Pool

def api():
    app.run()

if __name__ == "__main__":
    pool = Pool()
    pool.apply_async(api)
    
    time.sleep(3)
    proxy = requests.get('http://127.0.0.1:5000/random').text
    print()
    print('proxy: ', proxy)
    proxies = {
        'http': 'http://'+proxy,
        'https': 'https://'+proxy
    }

    req = requests.get('http://httpbin.org/get', proxies=proxies)
    print(req.text)
    
    pool.close()
    pool.join()