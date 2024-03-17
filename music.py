import json
import random
from selenium import webdriver
import time
import pickle
from selenium.webdriver.common.by import By
import os
# from win10toast import ToastNotifier

# toaster = ToastNotifier()
def show_message(message,duration=5):
    # toaster.show_toast("音乐播放器",
    #                 message,
    #                 duration=duration)
    print(message)

def play(music):
    global playsData
    url=music["href"]
    browser = webdriver.Edge()
    browser.get("https://music.163.com")
    if os.path.exists('cookies'):
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
    browser.get(url)
    print("已刷新网页.")
    time.sleep(1)
    browser.switch_to.frame("g_iframe")
    browser.find_element(By.CSS_SELECTOR,".u-btn2").click()
    show_message("开始播放:"+music['name'])
    print(f"正在播放:{music['name']}")
    browser.switch_to.default_content()
    progress=100*browser.find_element(By.CSS_SELECTOR,".barbg>.cur").size['width']/browser.find_element(By.CSS_SELECTOR,".barbg").size['width']
    while progress<98:
        time.sleep(0.1)
        progress=100*browser.find_element(By.CSS_SELECTOR,".barbg>.cur").size['width']/browser.find_element(By.CSS_SELECTOR,".barbg").size['width']
        print(progress)
    playsData.append({"music":music,"time":time.time()})
    browser.quit()

if not os.path.exists('cookies'):
    raise Exception("请先登录网易云音乐.(运行refresh程序)")

f=open("musics.json",'r',encoding='utf-8')
musicData=json.loads(f.read())
f.close()
if os.path.exists('plays.json'):
    f=open("plays.json",'r',encoding='utf-8')
    playsData=json.loads(f.read())
    f.close()
else:
    playsData=[]


for i in playsData:
    if time.time()-i['time']<3600*24*2:
        musicData.remove(i)
try:
    show_message("程序启动",3)
    play(musicData[random.randint(0,len(musicData)-1)])
except ZeroDivisionError:
    raise Exception("播放失败,请检查登录情况.")

f=open("plays.json",'w',encoding='utf-8')
f.write(json.dumps(playsData,indent=4,ensure_ascii=False))
f.close()
