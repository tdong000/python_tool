#  coding=utf-8

from Tkinter import *
from ScrolledText import ScrolledText
import urllib
import requests
import re
import threading

url_name = []
a = 1


def get():
    global a
    hd = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'}
    url = 'http://www.budejie.com/video/' + str(a)
    # varl.set('以获取第%d页的视频', a)
    html = requests.get(url, headers=hd).text
    url_content = re.compile(r'(<div class="j-r-list-c">.*?</div>.*?</div>)', re.S)
    url_contents = re.findall(url_content, html)
    # print url_contents
    for i in url_contents:
        url_reg = r'data-mp4="(.*?)">'
        url_items = re.findall(url_reg, i)
        # print url_items # 获取视频地址
        if url_items:
            name_reg = re.compile(r'<a href="/detail-.{8}?.html">(.*?)</a>', re.S)
            name_items = re.findall(name_reg, i)  # 获取视频名称
            # print name_items
            for j, k in zip(name_items, url_items):
                url_name.append([j,k])
                print j, k
    return url_name

id = 1  # 视频个数


def write():
    global id
    while id < 10:
        url_name = get()
        for i in url_name:
            urllib.urlretrieve(i[1], 'video\\%s.mp4' % (i[0].decode('utf-8').encode('gbk')))
            text.insert(END,str(id)+'.'+i[1]+'\n'+i[0]+'\n')
            url_name.pop(0)
            id += 1
    varl.set('Complete!!!')


def start():
    th = threading.Thread(target=write)
    th.start()


root = Tk()
root.title("爬框")
text = ScrolledText(root, font=('微软雅黑',10))
text.grid()
button = Button(root, text='开始爬去', font=('微软雅黑',10), command=start)
button.grid()

varl = StringVar()
label = Label(root, font=('微软雅黑',10), fg='red', textvariable=varl)
label.grid()
varl.set("已准备...")
root.mainloop()
