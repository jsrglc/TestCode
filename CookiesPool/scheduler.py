import time
from multiprocessing import Process
from api import app
from generator import GithubCookiesGenerator
from tester import GithubValidTester
from RedisDB import RedisClient

if __name__ == "__main__":
    redis = RedisClient('accounts', 'github')
    redis.set('jsrglc', 'liuchennuaa2010')
    redis.set('js', 'liu')

    print('Cookies 生成进程开始运行 ')
    generator = GithubCookiesGenerator()
    generator.run()
    print('Cookies 生成完成 ')

    
    print('Cookies 检测进程开始运行 ')
    tester = GithubValidTester()
    tester.run()
    print('Cookies 检测完成 ')

    app.run()