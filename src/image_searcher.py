import requests
import time
import os
import re
import random
import string
from pathlib import Path

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from bs4 import BeautifulSoup

QUERY        = "dogs" #search word
LIMIT_DL_NUM = 100 #number of images

RETRY_NUM = 3
TIMEOUT   = 3

def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") #hide browser
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    url = f'https://www.google.com/search?q={QUERY}&tbm=isch'
    browser.get(url)

    # 表示されるサムネイル画像をすべて取得する
    thumbnail_elements = browser.find_elements(By.CLASS_NAME, 'Q4LuWd')

    # 取得したサムネイル画像数を数える
    count = len(thumbnail_elements)
    print(count)

    #取得したい枚数以上になるまでスクロール
    while count < LIMIT_DL_NUM:
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(2)

        thumbnail_elements = browser.find_elements(By.CLASS_NAME, 'Q4LuWd')
        count = len(thumbnail_elements)
        print(count)

    HTTP_HEADERS = {'User-Agent' : browser.execute_script('return navigator.userAgent;')}
    print(HTTP_HEADERS)

    image_urls = []

    for index, thumbnail_element in enumerate(thumbnail_elements):
        image_url     = thumbnail_element.get_attribute('src')
        is_clicked = False

        for i in range(RETRY_NUM):
            try:
                if not is_clicked:
                    thumbnail_element.click()
                    time.sleep(1)
                    is_clicked = True
            except NoSuchElementException:
                print(f'NoSuchElementException')
                continue
            except Exception:
                print('Unknown error occurred.')
                break
        
            try:
                image_element = browser.find_element(By.CLASS_NAME, 'iPVvYb')
                image_url     = image_element.get_attribute('src')

                if re.match(r'data:image', image_url):
                    print(f'URLが変わるまで待ちましょう。{i+1}回目')
                    time.sleep(2)
                    if i+1 == RETRY_NUM:
                        print(f'urlは変わりませんでしたね。。。')
                    continue
                else:
                    print(f'image_url: {image_url}')
                    extension = get_extension(image_url)

                    if extension:
                        image_urls.append(image_url)
                        print(f'urlの保存に成功. 保存したurl : {index}個')

                    # jpg jpeg png 以外はダウンロードしない
                    else:
                        print('対象の拡張子ではありません')
                    break
            except NoSuchElementException:
                print(f'****NoSuchElementException*****')
                break

            except ElementClickInterceptedException:
                print(f'***** click エラー: {i+1}回目')
                browser.execute_script('arguments[0].scrollIntoView(true);', thumbnail_element)
                time.sleep(1)
            else:
                break

        if index+1 % 20 == 0:
            print(f'{i+1}件完了')
        time.sleep(1)

    project_dir = Path(__file__).resolve().parent.parent
    save_dir    = os.path.join(project_dir, 'data', QUERY)
    os.makedirs(save_dir, exist_ok=True)

    for image_url in image_urls:
        down_load_image(image_url, save_dir, 3, HTTP_HEADERS)

    browser.quit()

def get_extension(url:str):
    url_lower = url.lower()
    extension = re.search(r'\.jpg|\.jpeg|\.png', url_lower)
    if extension:
        return extension.group()
    else:
        return None
    
def randomname(n):
   randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
   return ''.join(randlst)
    
def down_load_image(url, save_dir, loop, http_header):
    result = False
    for i in range(loop):
        try:
            r = requests.get(url, headers=http_header, stream=True, timeout=10)
            r.raise_for_status()

            extension = get_extension(url)
            file_name = randomname(12)
            file_path = save_dir + '/' + file_name + extension

            with open(file_path, 'wb') as f:
                f.write(r.content)

            print(f'{url}の保存に成功')

        except requests.exceptions.SSLError:
            print('*****SSLエラー*****')
            break

        except requests.exceptions.RequestException as e:
            print(f'***** requests エラー ({e}): {i+1} 回目')
            time.sleep(1)
        else:
            result = True
            break
    return result

if __name__ == "__main__":
    main()

    

