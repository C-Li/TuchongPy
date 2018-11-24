import json
import requests
import os
import time
import shutil

# 浏览器请求头（大部分网站没有这个请求头会报错、请务必加上哦）
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}

f = open('items.json', 'r', encoding='UTF-8')  # json文件的路径
jsonArray = json.load(f)

filePath = r"D:\\"  # 下载到D盘
path = "imgs"
if(os.path.exists(filePath+path)):
    shutil.rmtree(filePath+path)    # 删除文件夹
os.makedirs(os.path.join(filePath, path))  # 创建一个存放套图的文件夹

i = 0   # 照片计数
j = 0   # 子文件夹名
yes = False
for obj in jsonArray:
    yes = False

    # 在评论中检索关键字
    keyWords = ['优秀', '棒']
    for comment in obj['comments']:
        if comment != None:
            for key in keyWords:
                if key in comment:
                    yes = True

    # 如果点赞数占浏览量的10%以上（大概就是优秀的作品）或者评论中含有关键字，就下载这幅作品
    if int(obj['favorites']) > 0:
        if int(obj['views'])/int(obj['favorites']) <= 10 or yes:
            # 新建子文件夹
            if(not os.path.exists(filePath+path+'/'+str(j))):
                os.makedirs(filePath+path+'/'+str(j))
            os.chdir(filePath+path+'/'+str(j))  # 切换到上面创建的文件夹
            k = 0
            # 写入作品信息
            info = "info.txt"
            ft = open(info, 'w')
            ft.write('title:'+obj['title'])
            ft.write('\nurl:'+obj['url'])
            ft.write('\nfavorites:'+str(obj['favorites']))
            ft.close()
            # 下载写入照片
            for url in obj['pic_urls']:
                name = str(k)
                img = requests.get(url, headers=headers)    # 请求图片
                # 写入多媒体文件必须要 b 这个参数,b代表二进制格式
                f = open(name+'.jpg', 'ab')
                f.write(img.content)        # 多媒体文件要使用content
                f.close()
                print('img '+str(i) + " downloaded")
                i += 1
                k += 1
            j += 1

print('done!')
