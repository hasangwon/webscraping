import csv
from bs4 import BeautifulSoup
from selenium import webdriver
import time

hdr = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36"}

# 크롤링 -------------------------------------------------------------------
print('시작')
searchList = []
searchList.append(['제목','주소'])
url = 'https://bitcoins.tistory.com/'  # 사이트 입력
driver = webdriver.Chrome(r"/Users/hasangwon/chromedriver")
time.sleep(1)
driver.get(url)
driver.implicitly_wait(3000)

# 스크롤 끝까지 
SCROLL_PAUSE_TIME = 2
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight-50);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    
html = driver.page_source
soup = BeautifulSoup(html)
r = soup.select('div.post-item') # 반복되는 선택자 입력

for x in r :
    temp = []
    try : 
        temp.append(x.select_one('a span.title').text)   # 크롤링 항목 1
        temp.append(x.select_one('a').attrs['href']) # 크롤링 항목 2
        searchList.append(temp) 
    except AttributeError as e :
        searchList.append(temp)  

driver.close()

# CSV 저장-------------------------------------------------------------------------
print('CSV에 저장')
f = open(f'/Users/hasangwon/Desktop/crawling/file.csv', 'w', encoding='utf-8', newline='')
csvWriter = csv.writer(f)
for i in searchList:
    csvWriter.writerow(i)
f.close()
print('완료')      