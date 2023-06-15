from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

driver_url="D:\chromedriver\chromedriver.exe"
s=Service(driver_url)

page_url="https://leetcode.com/problemset/all/?page="

def get_a_tags(url):
    driver=webdriver.Chrome()
    print(url)
    driver.get(url)
    time.sleep(10)
    all_a=driver.find_elements(By.TAG_NAME,"a")
    arr=[]
    for link in all_a:
        try:
            if "/problems/" in link.get_attribute("href"):
                arr.append(link.get_attribute("href"))
        except:
            pass
    # driver.close()
    arr=list(set(arr))
    driver.quit()
    print(len(arr),end=" ")
    return arr
links=[]
for i in range(20,21):
    a=get_a_tags(page_url+str(i))
    for link in a:
        links.append(link)
    links=list(set(links))
    print((len(links)))

    links=list(set(links))

print("Total length",end=" ")
print((len(links)))
with open("lc.txt",'a') as f:
    for link in links:
        f.write(link+"\n")
        # print(link)
