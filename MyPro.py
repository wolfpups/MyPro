from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import itchat,pygame,time

flag="THIS SHADE/SIZE: SOLD OUT" #缺货标志
proFile="缺货产品URL.txt"        #需要检测的产品链接文件
wxFile="微信备注名.txt"          #需要推送消息的微信列表
musFile="v2.mp3"                 #提示音文件

def catchUrl(url):
    #捕获产品链接,返回是否有货标志
    options = Options()
    options.add_argument('--headless')# 无头模式启动
    options.add_argument('--disable-gpu')# 谷歌文档提到需要加上这个属性来规避bug
    driver= webdriver.Chrome(options=options)
    driver.get(url)#获取页面
    text=driver.find_element_by_class_name('sold-out').text
    driver.quit()#退出关闭浏览器
    return text

def openBrowser(url):
    driver= webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)
    driver.quit()
def sendMessage(url):
    #向微信推送货物消息
    wxs=open(wxFile).readlines()#读取接受微信消息列表
    msg=proName(url)+"有货,链接："+url
    for wx in wxs:
        user=itchat.search_friends(name=wx.strip())
        userName = user[0]['UserName']
        itchat.send(msg=msg,toUserName=userName)

def playMusic():
    pygame.mixer.init()
    track = pygame.mixer.music.load(musFile)
    pygame.mixer.music.play(-1)

def proName(url):
    return  (' '.join([word.capitalize() for word in url.split("/")[-1].split("-")])).rstrip()


itchat.auto_login(hotReload=True)

while True:
    urls=open(proFile).readlines()#读取url列表
    newUrls=[]#未补货的列表
    for url in urls:
        if flag==catchUrl(url):
            newUrls.append(url)
            print(proName(url) + "没货\n链接："+url)
        else:
            sendMessage(url)
            playMusic()
            print(proName(url)+"有货\n链接："+url)
    if newUrls is None:
        break
    open(proFile,'w').write('\n'.join(newUrls))
    
