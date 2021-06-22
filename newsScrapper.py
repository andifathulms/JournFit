import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def timeCounter(start):
    now = time.perf_counter()
    return f"{now-start:0.5f}"

def requestURL(url,arg):
    print(f'Request adress for {arg} ...')
    start = time.perf_counter()
    
    for attempt in range(1,11):
        try:
            print(f"Attempt no: {attempt} ...")
            req = requests.get(url,timeout=20, headers={'User-Agent': 'Mozilla/5.0','Connections':'close'})
            print(f"Success! Time : {timeCounter(start)} \n")
            return req.content
        except:
            print(f"Fail! Time : {timeCounter(start)} \n")
            time.sleep(0.25)
            continue
        break
    print("Fail! Reached maximum attempt")

def scrapingContent(url1,url2,url3):
    options = Options()
    options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    options.headless = True
    start = time.perf_counter()
    print("Open Driver..")
    driver = webdriver.Chrome("C:\\Users\\LENOVO\\chromedriver.exe", options = options)
    print("Request URL1..")
    driver.get(url1)
    print(f"Success! Time : {timeCounter(start)} \n")
    """
    for i in range(1,15):
        rowList = []
        for j in range(1,10):
            xpath = f'/html/body/div[3]/div/div/div[2]/div/div/div/standards/div/div[2]/div/div[2]/div[1]/table/tbody/tr[{i}]/td[{j}]'
            cell = driver.find_elements_by_xpath(xpath)
            rowList.append(cell[0].text)
        colList.append(rowList)
    """
    cont = []
    link = []
    for i in range(1,10):
        xpath = f'/html/body/main/div[4]/div[1]/div[{i}]/div[3]/a[1]'
        cell = driver.find_elements_by_xpath(xpath)
        try:
            cont.append(cell[0].text)
            link.append(cell[0].get_attribute('href'))
        except: pass
    
    print("Request URL2..")
    driver.get(url2)
    print(f"Success! Time : {timeCounter(start)} \n")

    cont1 = []
    link1 = []
    for i in range(1,10):
        xpath = f'/html/body/div[2]/div[2]/div/div[2]/div/div/main/div/div[1]/article[{i}]/div/div[2]/header/h2/a'
        cell = driver.find_elements_by_xpath(xpath)
        try:
            cont1.append(cell[0].text)
            link1.append(cell[0].get_attribute('href'))
        except: pass
    
    print("Request URL3..")
    driver.get(url3)
    print(f"Success! Time : {timeCounter(start)} \n")

    cont2 = []
    link2 = []
    for j in range(1,15):
        for i in range(1,10):
            xpath = f'/html/body/div[3]/div/section[{j}]/div/div/div[1]/ul/li[{i}]/div/div/a'
                      #/html/body/div[3]/div/section[3]/div/div/div/ul/li[2]/div/div/a
            cell = driver.find_elements_by_xpath(xpath)
            try:
                cont2.append(cell[0].get_attribute("innerText"))
                link2.append(cell[0].get_attribute('href'))
            except: pass
       
    container = [cont,link,cont1,link1,cont2,link2]
    #print(container)
    driver.quit()
    return container
    #print(link)

if __name__ == '__main__':
    scrapingContent("https://www.health.com/fitness","https://www.t-nation.com/training/")