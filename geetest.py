from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

EMAIL = 'test@test.com'
PASSWORD = '123456'

class CrackGeetest():
    def __init__(self):
        self.url = 'https://account.geetest.com/login'
        self.email = EMAIL
        self.password = PASSWORD

        opt = webdriver.ChromeOptions()
        opt.headless = False
        self.browser = webdriver.Chrome(options=opt)
        self.wait = WebDriverWait(self.browser, 10)
    
    def __del__(self):
        self.browser.close()
    
    def get_geetest_button(self):
        """
        return: 
            button: 初始验证按钮对象
        """
        button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.geetest_btn .geetest_radar_tip')))
        return button
    
    def get_position(self):
        """
        return:
            (top, bottom, left, right): 验证码位置元组
        """
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_img')))
        time.sleep(2)
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
        return (top, bottom, left, right)

    def get_geetest_image(self, filename='captcha.png'):
        """
        Args:
            filename: 图片名称
        return:
            captcha: 验证码图片对象
        """
        top, bottom, left, right = self.get_position()
        print(' 验证码位置：', top, bottom, left, right)
        screenshot = self.browser.get_screenshot_as_file(filename)
        captcha = screenshot.crop((left, top, right, bottom))
        return captcha
    
    def get_slider(self):
        """
        return:
            slider: 滑块对象
        """
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
        return slider

    def is_pixel_equal(self, image1, image2, x, y):
        """
        Args:
            image1: 图片 1
            image2: 图片 2
            x: 位置 x
            y: 位置 y
        return:
            两个像素是否相同
        """
        # 取两个图片的像素点
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        threshold = 60
        if abs(pixel1[0] - pixel2[0]) <threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False
    
    def get_gap(self, image1, image2):
        """
        Args：
            image1: 不带缺口图片
            image2: 带缺口图片
        return:
            left: 缺口偏移量
        """
        left = 60
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1, image2, i, j):
                    left = i
                    return left
        return left
        
    def get_track(self, distance):
        """
        Args:
            distance: 偏移量
        return:
            tracks: 移动轨迹
        """
        # 移动轨迹
        tracks = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.2
        # 初始速度
        v = 0

        while current < distance:
            if current < mid:
                # 加速度为正 2
                a = 2
            else:
                # 加速度为负 3
                a = -3
            # 初速度 v0
            v0 = v
            # 当前速度 v = v0 + at
            v = v0 + a * t
            # 移动距离 x = v0t + 1/2 * a * t^2
            move = v0 * t + 0.5 * a * t * t
            # 当前位移 
            current += move
            # 加入轨迹
            tracks.append(round(move))
        return tracks

    def move_to_gap(self, slider, tracks):
        """
        拖动滑块到缺口处
        
        Args:
            slider: 滑块
            tracks: 轨迹
        """
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in tracks:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.browser).release().perform()
    
    def main(self):
        self.browser.get(self.url)
        
        email_ele = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.content-outter > div > div.inner-conntent > div:nth-child(3) > div > form > div:nth-child(1) > div > div > input')))
        passwd_ele =self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.content-outter > div > div.inner-conntent > div:nth-child(3) > div > form > div:nth-child(2) > div > div > input')))
        email_ele.clear()
        email_ele.send_keys(self.email)
        passwd_ele.clear()
        passwd_ele.send_keys(self.password)
        self.browser.get_screenshot_as_file('result1.png')

        time.sleep(1)
        button = self.get_geetest_button()
        button.click()

#        image1 = self.get_geetest_image('image1_t.png')
#        slider = self.get_slider()
#        slider.click()
#        image2 = self.get_geetest_image('image2_t.png')
#        left = self.get_gap(image1, image2)
        
#        tracks = self.get_track(left)

#        self.move_to_gap(slider, tracks)
        time.sleep(1)
        self.browser.get_screenshot_as_file('result2.png')

if __name__ == "__main__":
    crackGee = CrackGeetest()
    crackGee.main()