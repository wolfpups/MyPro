from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
import selenium.webdriver.support.ui as UI
from fake_useragent import UserAgent
import itchat,pygame,time,random


proFile="缺货产品URL2.txt"        #需要检测的产品链接文件
wxFile="微信备注名.txt"          #需要推送消息的微信列表
musFile="v2.mp3"                 #提示音文件

ua=UserAgent(verify_ssl=False)
options = Options()
#options.add_argument('--headless')# 无头模式启动
options.add_argument('--disable-gpu')# 谷歌文档提到需要加上这个属性来规避bug
options.add_argument('log-level=3')
options.add_argument(ua.random)#随机获取UserAgent

def closeOtherHandles(driver):
    #关闭其它标签
    handles=driver.window_handles
    otherHandles=handles[1:]
    for handle in otherHandles:
        driver.switch_to.window(handle)
        driver.close()
    driver.switch_to.window(handles[0])


def catchUrl(url):
    #捕获产品链接,返回是否有货标志
    result=False
    try:
        driver= webdriver.Chrome(options=options)
        #closeOtherHandles(driver)
        driver.get(url)#获取页面
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
        return result


def sendMessage(url):
    #向微信推送货物消息
    #wxs=open(wxFile).readlines()#读取接受微信消息列表
    wxs=getList(wxFile)
    msg=title+"有货,链接："+url
    for wx in wxs:
        user=itchat.search_friends(name=wx.encode('utf-8').decode('utf-8-sig').strip())
        userName = user[0]['UserName']
        itchat.send(msg=msg,toUserName=userName)

def playMusic():
    #播放提示音
    pygame.mixer.init()
    pygame.mixer.music.load(musFile)
    pygame.mixer.music.play(60)#-1一直播放


def getList(filename):
    lines=open(filename,encoding='UTF-8-sig').readlines()
    lines=[line.strip() for line in lines if line.strip()!='']
    return lines


if getList(wxFile)==[]:
    print("微信联系人列表为空，要用微信提醒请在"+wxFile+"中添加联系人")
else:
    itchat.auto_login(hotReload=True)
    


while True:
    urls=getList(proFile)
    newUrls=[]#未补货的列表
    for url in urls:
        if catchUrl(url):
            if getList(wxFile)!=[]:
                sendMessage(url)
            #playMusic()
            newUrls.append(url)#测试用,发布时需要删除
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +' 有货 链接:'+url)
        else:
            newUrls.append(url)
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +' 没货 链接:'+url)
        rn=random.randint(30,120)#每条链接之间随机等待60-180秒
        print('等待: '+str(rn)+' 秒')
        #time.sleep(rn)
    if newUrls==[]:
        print("没有新的链接需要检测,添加链接后重新运行程序")
        open(proFile,'w',encoding='utf8').write('\n'.join(newUrls))
        break
    open(proFile,'w',encoding='utf8').write('\n'.join(newUrls))
