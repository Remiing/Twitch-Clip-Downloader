import re
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from urllib.request import urlretrieve


def get_vid_data(clip_list):
    f = open('log.txt', 'a', encoding='UTF-8')
    print('webdriver Preparing')
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    print('webdriver ready')
    for i, url in enumerate(clip_list, start=1):
        print(f'{i}/{len(clip_list)}\t{url}')
        driver.get(url)
        WebDriverWait(driver, 10).until(expected_conditions.title_contains(' - Twitch'))
        vid_title = driver.title
        vid_url = driver.find_element_by_tag_name('video').get_attribute('src')
        if vid_url:
            print(f'├─{vid_title}')
            savename = re.sub(r'[\/:*?"<>|]', '', vid_title).replace(' - Twitch', '') + '.mp4'
            path = './clips/'
            urlretrieve(vid_url, path + savename)
            print(f'└─download success')
            f.write(f'{url} success\n')
            f.write(f'└─{vid_title}\n')

        else:
            f.write(f'{url} fail\n')
            print(f'└─download fail')


def read_clip_list():
    try:
        os.mkdir('./clips')
    except FileExistsError as e:
        pass
    f = open('clip_list.txt', 'r')
    clip_list = f.read().split('\n')
    clip_list = list(filter(None, clip_list))
    return clip_list


if __name__ == '__main__':
    clip_list = read_clip_list()
    get_vid_data(clip_list)
