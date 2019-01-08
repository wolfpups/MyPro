from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import itchat,pygame,time,datetime,sys


proFile="缺货产品URL.txt"        #需要检测的产品链接文件
wxFile="微信备注名.txt"          #需要推送消息的微信列表
musFile="v2.mp3"                 #提示音文件
title=""

options = Options()
options.add_argument('--headless')# 无头模式启动
options.add_argument('--disable-gpu')# 谷歌文档提到需要加上这个属性来规避bug
options.add_argument('log-level=3')

def catchUrl(url):
    #捕获产品链接,返回是否有货标志
    global title
    driver= webdriver.Chrome(options=options)
    result=False
    try:
        driver.get(url)#获取页面
        addButton=driver.find_element_by_class_name("product-full__add-button")
        soldOutLi=driver.find_element_by_class_name("sold-out")
        addDisplayed=addButton.is_displayed()
        soldOutDisplayed=soldOutLi.is_displayed()
        if addDisplayed and soldOutDisplayed==False:
            result=True#有货
        elif soldOutDisplayed and addDisplayed==False:
            result=False#没货
        else:
            result=False
        title=driver.title.split(" | ")[0]
    except:
        result=False
    finally:
        driver.quit()#退出关闭浏览器
        return result


def sendMessage(url):
    #向微信推送货物消息
    wxs=open(wxFile).readlines()#读取接受微信消息列表
    wxs=getList(wxFile)
    msg=title+"有货,链接："+url
    for wx in wxs:
        user=itchat.search_friends(name=wx.strip())
        userName = user[0]['UserName']
        itchat.send(msg=msg,toUserName=userName)

def playMusic():
    #播放提示音
    pygame.mixer.init()
    track = pygame.mixer.music.load(musFile)
    pygame.mixer.music.play(-1)

def getList(filename):
    lines=open(filename,encoding='utf8').readlines()
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
            playMusic()
            print(title+"有货\n链接："+url+"\n")            
        else:
            newUrls.append(url)
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"  "+title + " 没货\n链接："+url+"\n")
        time.sleep(int(getList("延迟时间.txt")[0]))
    if newUrls==[]:
        print("没有新的链接需要检测,添加链接后重新运行程序")
        break
    open(proFile,'w',encoding='utf8').write('\n'.join(newUrls))
