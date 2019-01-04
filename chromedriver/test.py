from selenium import webdriver
from selenium.webdriver.chrome.options import Options
url="https://www.esteelauder.com./product/14324/61151/product-catalog/whats-new/gifts/detox-glow/for-vibrant-healthy-looking-skin"
#url="https://www.esteelauder.com/product/14324/60135/product-catalog/whats-new/gifts/repair-renew/wake-up-to-more-youthful-radiant-looking-skin"
options = Options()
# 无头模式启动
options.add_argument('--headless')
# 谷歌文档提到需要加上这个属性来规避bug
options.add_argument('--disable-gpu')
# 修改User-Agent
#options.add_argument('User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/62.0.3202.89 Safari/537.36')
# 初始化实例
driver= webdriver.Chrome(options=options)
driver.set_window_size(1920,1080)
driver.get(url)
driver.refresh()
#driver.maximize_window()
driver.get_screenshot_as_file("proImg.png")
#driver.close()
driver.quit()
