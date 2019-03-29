from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
import selenium.webdriver.support.ui as UI
from fake_useragent import UserAgent
import itchat,pygame,time,random

ua=UserAgent(verify_ssl=False)
options = Options()
#options.add_argument('--headless')# 无头模式启动
options.add_argument('--disable-gpu')# 谷歌文档提到需要加上这个属性来规避bug
options.add_argument('log-level=3')
options.add_argument(ua.random)
url1='https://www.esteelauder.com/product/14324/59459/product-catalog/whats-new/gifts/repair-and-renew/for-firmer-radiant-looking-skin'
url2='https://www.esteelauder.com/product/681/61891/product-catalog/skincare/daywear/anti-oxidant-72h-hydration-sorbet-creme-spf-15'

driver= webdriver.Chrome(options=options)
driver.get(url2)
driver.maximize_window()
driver.save_screenshot('a.png')
ActionChains(driver).move_by_offset(10, 50).click().perform()
driver.save_screenshot('b.png')
addButton=driver.find_element_by_class_name("product-full__add-button")
addButton.click()
while False:
     try:
        #options.add_argument(ua.random)#随机获取UserAgent
        driver= webdriver.Chrome(options=options)
        #closeOtherHandles(driver)
        driver.get(url1)#获取页面
        
        #UI.WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'loyalty_popover__link-container')))
        time.sleep(3)
        ActionChains(driver).move_by_offset(10, 50).click().perform()
        time.sleep(3)    
        addButton=driver.find_element_by_class_name("product-full__add-button")#获取Add To Bag按钮
        cartCount=driver.find_element_by_class_name("utility-nav__cart-count")#获取CartCount
        addButton.click()#点击Add To Bag按钮,有货页面cartCount会加1，没货页面将触发异常
        time.sleep(3)
        if cartCount.text!='':
            result=True
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +' --- '+cartCount.text)
     except BaseException as err:
        print(err)
        result=False
     finally:
        driver.close()#关闭当前窗口
        driver.quit()#关闭浏览器

while False:
    driver= webdriver.Chrome(options=options)
#获取页面
#time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    driver.get(url2)#获取页面
#UI.WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, 'loyalty_popover__link-container')))
#ActionChains(driver).move_by_offset(10, 10).click().perform()
    time.sleep(3)
    #driver.close()
    driver.quit()
    
while False:
    driver.get(url2)
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
    rn=random.randint(60,180)#随机等待60-180秒
    print('等待: '+str(rn)+' 秒')
    time.sleep(3)
    driver.close()
    driver.quit()
    #ActionChains(driver).move_by_offset(10, 10).click().perform()
    #loyalty_popover__link-container  "loyalty_popover"
    js1 = 'document.getElementsByClassName("loyalty_popover__link-container")[0].style.display="none";'
    js2 = 'document.getElementById("cboxLoadedContent").style.display="none";'
    js3 = 'document.getElementById("cboxContent").style.display="none";'
    js4 = 'document.getElementById("cboxWrapper").style.display="none";'
    js5 = 'document.getElementById("colorbox").style.display="none";'
    js6 = 'document.getElementById("cboxOverlay").style.display="none";'
    js7 = 'document.getElementById("cboxOverlay").style.display="none";'
    js='document.getElementsByClassName("loyalty_popover__link-container")[0].style.display="none";document.getElementById("cboxLoadedContent").style.display="none";document.getElementById("cboxContent").style.display="none";document.getElementById("cboxWrapper").style.display="none";document.getElementById("colorbox").style.display="none";document.getElementById("cboxOverlay").style.display="none";'
    
    handles=driver.window_handles
    otherHandles=handles[1:]
    for handle in otherHandles:
        driver.switch_to_window(handle)
        driver.close()
    
    
    
    
    