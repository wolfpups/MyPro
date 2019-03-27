from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
#options.add_argument('--headless')# 无头模式启动
options.add_argument('--disable-gpu')# 谷歌文档提到需要加上这个属性来规避bug
options.add_argument('log-level=3')
options.add_argument('Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36')
url1='https://www.esteelauder.com/product/14324/59459/product-catalog/whats-new/gifts/repair-and-renew/for-firmer-radiant-looking-skin'
url2='https://www.esteelauder.com/product/681/61891/product-catalog/skincare/daywear/anti-oxidant-72h-hydration-sorbet-creme-spf-15'

driver= webdriver.Chrome(options=options)
driver.get(url2)#获取页面
#time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
while True:
    driver.refresh()
    addButton=driver.find_element_by_class_name("product-full__add-button")
    cartCount=driver.find_element_by_class_name("utility-nav__cart-count")
    #print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +'点击前：'+cartCount.text)
    try:
        addButton.click()
        if cartCount.text!='':
           # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +'点击后:'+cartCount.text)
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +'有货'+cartCount.text)
           # break
    except:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +'没货')
    time.sleep(60)