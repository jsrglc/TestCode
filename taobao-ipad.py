from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from pymongo import MongoClient
from pyquery import PyQuery as pq

def main(browser, max_page, collection):
    wait = WebDriverWait(browser, 10)
    for page in range(1, max_page+1):
        print('parsing page:', page, ' ....')
        if page > 1:
            J_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input.input.J_Input')))
            J_submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'span.btn.J_Submit')))
            J_input.clear()
            J_input.send_keys(str(page))
            J_submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active span'), str(page)))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
        get_products(browser, collection)

def get_products(browser, collection):
    doc = pq(browser.page_source)
    items = doc('.m-itemlist .items .item').items()
    print('number of items: ', len(items))
    for item in items:
        product = {}
        product['image'] = 'http:' + item.find('.pic-box-inner .pic .img').attr('data-src')
        product['price'] = item.find('.ctx-box .price.g_price strong').text()
        product['deal'] = item.find('.ctx-box .deal-cnt').text()
        product['title'] = item.find('.row.row-2.title').text().strip()
        product['shop'] = item.find('.shopname span').text()
        product['location'] = item.find('.location').text()
        
        collection.insert_one(product) # save to MongoDB

if __name__ == "__main__":
    opt = webdriver.ChromeOptions()
#    opt.headless = False
#    opt.add_argument("--start-maximized")
#    opt.add_argument('--disable-gpu')
    opt.add_experimental_option('excludeSwitches', ['enable-automation'])
    browser = webdriver.Chrome(options=opt)

    keyword = 'ipad'    
    url = 'https://s.taobao.com/search?q=' + keyword
    browser.get(url)
    
    max_page = 1   # max page number to search
    collection = MongoClient().taobao.products # initialize MongoDB
    main(browser, max_page, collection)
    browser.close()
