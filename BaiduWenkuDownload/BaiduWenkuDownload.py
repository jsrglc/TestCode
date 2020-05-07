from pyquery import PyQuery as pq
from selenium import webdriver
import requests, time, os

def get_browser(url):
    opt = webdriver.ChromeOptions()
#    opt.headless = True
    opt.add_argument("--window-size=1920,1080")
    opt.add_argument("--start-maximized")
    opt.add_argument('--disable-gpu')
    opt.add_argument('User-Agent="Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"')
    browser = webdriver.Chrome(options=opt)
    
    browser.get(url)
    browser.implicitly_wait(3)
    return browser

def BaiduWenkuDL(url, dirname):
    browser = get_browser(url)

    time.sleep(1)
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight*0.6)')
    next_click = browser.find_element_by_xpath('//*[@id="html-reader-go-more"]/div[2]/div[1]/span')
    next_click.click()
    time.sleep(3)
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight*0.9)')

    doc = pq(browser.page_source)
    browser.close()

    items = doc('#flow-ppt-wrap > div > div > div[class*=ppt-page-item]')
    print('共有页面：', len(items), '，开始下载...')
    for item in items.items():

        filename = item.attr('class').split('pageNo-')[-1].split(' ')[0] + '.jpg'

        src = item.find('div > img').attr('src')
        if not src:
            src = src = item.find('div > img').attr('data-src')
        save_pic(src, dirname, filename)

def save_pic(src, dirname, filename):
    if not os.path.exists(dirname):
        os.mkdir(dirname)

    print('正在下载 url：{} file: {}'.format(src, filename))
    content = requests.get(src).content
    with open(dirname + '/' + filename, 'wb') as f:
        f.write(content)

if __name__ == "__main__":
    url = 'https://wenku.baidu.com/view/e04082e96aec0975f46527d3240c844769eaa02e'
    dirname = 'pictures'

    BaiduWenkuDL(url, dirname) 