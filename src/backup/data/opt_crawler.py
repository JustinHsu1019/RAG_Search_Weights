from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import time
import keyboard
import json

chromedriver_path = 'data/chromedriver.exe'

# 歐趴糖中政治大學評價路徑
website = 'https://www.1111opt.com.tw/search-result/JTdCJTIydHlwZSUyMiUzQTAlMkMlMjJvcmRlciUyMiUzQSUyMi1tb2RpZnlfdGltZSUyMiUyQyUyMmNvbGxlZ2VfaWQlMjIlM0ExMDkzNTIyMCU3RA'

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(chromedriver_path))
driver.get(website)

contents = []

driver.add_cookie({"name": "__lt__cid", "value": "8e7dc95-7642-4c5a-b183-1d75c684420a"})
driver.add_cookie({"name": "__lt__sid", "value": "4902ecc3-797dfc1c"})
driver.add_cookie({"name": "_ga", "value": "GA1.1.1557211976.1713615666"})
driver.add_cookie({"name": "_ga_5EC5E2LZFV", "value": "GS1.1.1713615666.1.1.1713616879.60.0.0"})
driver.add_cookie({"name": "matrix", "value": "kqkjdudlc6ref1d1h3ho86bln8"})
driver.add_cookie({"name": "matrix-token", "value": "m0ezz70fdoqg42xhakk064puwa6s9y0ac4pzl20bks6hs9knw37g1ezrdstm6erxt"})
driver.get(website)

running = True
count = 1
while running:
    for i in range(1, 11):
        try:
            title = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div[1]/div[2]/div[{}]/div[1]/div[1]/div[2]/span'.format(i))
            description = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div[1]/div[2]/div[{}]/div[2]/div/span'.format(i))
            tag1 = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div[1]/div[2]/div[{}]/div[2]/ul/li[1]/span'.format(i))
            tag2 = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div[1]/div[2]/div[{}]/div[2]/ul/li[2]/span'.format(i))
            tag3 = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div[1]/div[2]/div[{}]/div[2]/ul/li[3]/span'.format(i))
            evaluation = tag1.text.replace('#', '').strip() + ', ' + tag2.text.replace('#', '').strip() + ', ' + tag3.text.replace('#', '').strip()

            content = {
                'title' : title.text,
                'description' : description.text,
                'evaluation' : evaluation
            }
            contents.append(content)
        except:
            continue

    if keyboard.is_pressed('s'):
        running = False
        
    print("OK", + count)
    count += 1
    time.sleep(3)

j = 1
# print(contents)
for content in contents:
    print(str(j) + ' ' + content['title'] + ' ' + content['description'] + ' ' + content['evaluation'])
    j += 1
    print('-' * 50)

with open('data/class_data.txt', 'w', encoding='utf-8') as f:
    json.dump(contents, f, ensure_ascii=False, indent=4)

driver.quit()
