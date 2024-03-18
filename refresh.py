import json
import os
from selenium import webdriver
import time
import pickle
from selenium.webdriver.common.by import By
# from win10toast import ToastNotifier

# toaster = ToastNotifier()
def show_message(message,duration=5):
    # toaster.show_toast("音乐播放器-刷新模块",
    #                 message,
    #                 duration=duration)
    print(message)

playlist_id = 9469163513 # 歌单id

browser = webdriver.Edge()
browser.get('https://music.163.com')

browser.maximize_window() # 最大化窗口

if os.path.exists('cookies'):
    show_message("尝试自动登录...",3)
    browser.delete_all_cookies()
    f=open('cookies','rb')
    cookies = pickle.load(f)
    print("正在加载cookies...")
    n=0
    for cookie in cookies:
        browser.add_cookie(cookie)
        n=n+1
        print(f"已加载cookies:",round(n/len(cookies)*100,2),"%")
    print("已加载cookies.")
    #刷新网页
    browser.refresh()
    
# 点击按钮
try:
    while True:
        try:
            while True:
                browser.find_element(By.CSS_SELECTOR,".mrc-modal-mask")
                time.sleep(0.5)
        except:
            pass
        browser.find_element(By.LINK_TEXT,'登录').click()
        show_message("请扫描登录二维码...",3)
except Exception as e:
    show_message("登录成功!",3)
    cookies = browser.get_cookies()
    with open('cookies','wb') as f:
        pickle.dump(cookies, f)
    
browser.get(f"https://music.163.com/#/my/m/music/playlist?id={playlist_id}")
time.sleep(3)
browser.switch_to.frame("g_iframe") # 切换到iframe
musics=browser.find_elements(By.CSS_SELECTOR,'.tt>.ttc>.txt>a')
Musics=[]
for music in musics:
    name=""
    n=1
    for i in music.text.split("\n"):
        if n%2==1:
            name+=i
        n+=1
    Musics.append({"href":music.get_attribute('href'),"name":name})


# 保存
f=open("musics.json",'w',encoding='utf-8')
f.write(json.dumps(Musics,ensure_ascii=False,indent=4))

show_message("刷新完毕!")

browser.quit()
