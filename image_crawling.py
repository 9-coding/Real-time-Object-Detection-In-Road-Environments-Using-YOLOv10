from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium
import time
import urllib.request
import os

print("selenium version: "+selenium.__version__)

KEYWORD = '포트홀' # 검색어
SAVE_NAME = 'pothole' # 파일에 저장될 이름
MAX_SIZE = 1000 # 저장할 파일의 최대 개수
SAVE_PATH = "crawling" # 크롤링한 이미지가 저장될 경로
IMG_CLASS = '.YQ4gaf'


# Reference: https://g3lu.tistory.com/28
"""
Requirements
Selenium library
: pip3 install -U selenium
  - selenium version이 4 이상이면 크롬드라이버 설치 필요x
"""

"""
initial settings
IMG_CLASS
- 내가 찾을 이미지의 썸네일 class값 지정
- 크롬의 개발자도구를 열어서 좌상단 화살표 아이콘 클릭.
- 이미지를 눌러 나오는 <img>의 class값을 점(.)을 포함해 확장자 형식으로 지정

"""


driver = webdriver.Chrome()
driver.get("https://www.google.co.kr/imghp?hl=ko&ogbl")

# 검색
input_element = driver.find_element(By.CLASS_NAME, "gLFyf") # gLFyf: 구글의 검색창 태그
input_element.send_keys(KEYWORD + Keys.ENTER)

#Scroll Down
elem = driver.find_element(By.TAG_NAME, 'body')
for i in range(60):
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.1)

#View More
try:
    view_more_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'mye4qd')))
    view_more_button.click()
    for i in range(80):
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1)
except:
    pass

images = driver.find_elements(By.CSS_SELECTOR, ".YQ4gaf")
links = [image.get_attribute('src') for image in images if image.get_attribute('src') is not None]
print(links)

n = 0
for k, i in enumerate(links):
    try:
        if n > MAX_SIZE:
            break
        url = i
        file = SAVE_NAME + str(n) + '.png'
        file_path = SAVE_PATH + '/' + file
        size = len(urllib.request.urlopen(url).read())

        # 너무 작은 크기의 이미지는 무시
        if size <= 1024:
            continue

        print(n, f'\tfile name: {file} \t size: {size}')
        urllib.request.urlretrieve(url, file_path)
        n += 1

    except Exception as e:
        print(e)
        continue

print('다운로드를 완료하였습니다.')
