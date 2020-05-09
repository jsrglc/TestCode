from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests, time, os
from SaveToWord import SaveToWord

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

def BaiduWenku_DOC_DL(url, outputDir):
    browser = get_browser(url)

    # 打开折叠页
    time.sleep(1)
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight*0.7)')
    next_click = browser.find_element_by_xpath('//*[@id="html-reader-go-more"]/div[2]/div[1]')
    next_click.click()
    
    # 获得总页码及题目
    doc = pq(browser.page_source)
    page = int(doc('span.page-count').text().split('/')[1])

    content = list( '0' * (page + 1))
    title = doc('#doc-tittle-0').text().replace('\n', '').replace(' ', '')
    content[0] = title
    print(' 正在下载：', title, ' 总页码：', page)

    # 依次输入页码，获取对应页面内容
    ipage = 1
    while ipage <= page:
        page_input = browser.find_element_by_xpath('//input[@class="page-input"]')
        page_input.clear()
        page_input.send_keys(ipage)
        page_input.send_keys(Keys.ENTER)

        doc = pq(browser.page_source)
        items = doc('#reader-container-inner-1 > div[class*=reader-page-]')
        for item in items.items():
            no_page = int(item.attr('class').split('-')[-1])

            content_item = item.text().replace('\n', '').replace(' ', '')
            if content_item and content[no_page] == '0':
                content[no_page] = content_item
                
                print(no_page)
                print('class: ',item.attr('class'))
                print('text: ', content_item)
                print('')

        time.sleep(1)
        if ipage == page:
            break
        ipage += 2
        if ipage > page:
            ipage = page
    
    browser.close()
    
    print(' 正在保存...')
    SaveToWord(content, outputDir).SaveParagraph()

if __name__ == "__main__":
    url = 'https://wenku.baidu.com/view/6f6ebaababea998fcc22bcd126fff705cd175c6a.html'
    outputDir = 'F:\\code-test\\Test-Area\\BaiduWenkuDownload\\docs\\'
    BaiduWenku_DOC_DL(url, outputDir) 