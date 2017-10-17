# coding=utf-8


import requests
from bs4 import BeautifulSoup
from lxml import etree
import os

headers = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}


def geturl():
    start_urls = ['http://www.ximalaya.com/dq/music/{}/'.format(pn) for pn in range(1, 85)]
    # print(start_urls)
    for start_url in start_urls:
        response = requests.get(start_url, headers=headers).text
        # print(response)
        soup = BeautifulSoup(response, 'lxml')
        for item in soup.find_all('div', class_='albumfaceOutter'):
            # print(item)
            # print(item.a['href'])
            # print(item.img['alt'])
            content = {
                'href': item.a['href'],
                'title': item.img['alt'],
                'img_url': item.img['src']
            }
            # print('正在下载{}'.format(item.img['alt']))
            get_music_file(item.a['href'],item.img['alt'])
            # break
        break


def get_music_file(url, title):
    response = requests.get(url, headers=headers).text
    num_list = etree.HTML(response).xpath('//div[@class="personal_body"]/@sound_ids')[0].split(',')
    # print(num_list)
    mkdir(title)
    os.chdir(r'D:\xmly\\'+title)
    for id in num_list:
        json_url = 'http://www.ximalaya.com/tracks/{}.json'.format(id)
        html = requests.get(json_url, headers=headers).json()
        m4a_url = html.get('play_path')
        download(m4a_url)


def mkdir(title):
    path = title.strip()
    print(path)
    is_exists = os.path.exists(os.path.join(r'D:\xmly\\', path))
    if not is_exists:
        # 创建一个叫做title的文件夹
        os.makedirs(os.path.join(r'D:\xmly\\', title), 'wb')
        return True
    else:
        return False


def download(url):
    content = requests.get(url).content
    name = url.split('/')[-1]
    with open(name, 'wb') as file:
        file.write(content)

if __name__ == '__main__':
    geturl()