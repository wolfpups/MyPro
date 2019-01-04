from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import pytesseract,os,itchat,pygame

url="https://www.esteelauder.com./product/14324/61151/product-catalog/whats-new/gifts/detox-glow/for-vibrant-healthy-looking-skin"



def catchUrl(url):
    fileName=url.split("/")[-1]+".png"
    options = Options()
    options.add_argument('--headless')# 无头模式启动
    options.add_argument('--disable-gpu')# 谷歌文档提到需要加上这个属性来规避bug
    driver= webdriver.Chrome(options=options)
    driver.set_window_size(1920,1080)#设置页面大小
    driver.get(url)#获取页面
    driver.refresh()#刷新页面使弹框消失
    driver.get_screenshot_as_file(fileName)#保存页面为图片
    driver.quit()#退出关闭浏览器
    return fileName

def cropImg(fileName):
    #裁剪网页图片
    newFileName="new"+fileName
    img = Image.open(fileName)#打开图像
    box=(1000,150,1700,800)#设置图像裁剪区域
    newImg=img.crop(box)#图像裁剪
    newImg.save(newFileName)#存储当前区域
    #os.remove(fileName)
    return newFileName

def imgToStr(fileName):
    #图片转换为文字
    text = pytesseract.image_to_string(Image.open(fileName))
    #os.remove(fileName)
    return text

def sendMessage(url):
    itchat.auto_login(hotReload=True)
    wxs=open("wx.txt").readlines()#读取wx消息列表
    msg=url.split("/")[-1]+"有货,链接："+url
    for wx in wxs:
        user=itchat.search_friends(name=wx.strip())
        userName = user[0]['UserName']
        itchat.send(msg=msg,toUserName=userName)

def palyMusic():
    pygame.mixer.init()
    track = pygame.mixer.music.load('MyPro/v2.mp3')
    pygame.mixer.music.play(-1)


while True:
    urls=open("urls.txt").readlines()#读取url列表
    newUrls=[]#未补货的列表
    for url in urls:
        fileName=catchUrl(url.strip())
        fileName=cropImg(fileName)
        text=imgToStr(fileName)
        if 'SOLD OUT' in text:
            newUrls.append(url)
        else:
            playMusic()
            sendMessage(url)
    open("urls.txt",'w').write('\n'.join(newUrls))
        
    
