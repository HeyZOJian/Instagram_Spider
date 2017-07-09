import requests
import re
import os
import time
import sys
import threading
import random
import string

import threadpool

headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, sdch, br'
    }

pool = threadpool.ThreadPool(10)


def get_user_info(username):
    """
    获取用户ID
    :param username: 用户名
    :return: 用户ID
    """
    url = 'https://www.instagram.com/' + username
    text = requests.get(url).text
    try:
        return re.findall('"owner": {"id": "(.*?)"},', text)[0]
    except :
        print('找不到该用户')


def download(user_name):

    """
    获取用户所有的照片和视频json信息
    :param username:
    :return:
    """
    if os.path.exists(user_name):
        os.chdir(user_name)
    else:
        os.mkdir(user_name)
        os.chdir(user_name)
        # os.mkdir('image')
        # os.mkdir('video')

    user_id = get_user_info(user_name)

    url = 'https://www.instagram.com/graphql/query/'

    payload = {'query_id': 17880160963012870,
               'id': user_id,
               'first': 0}

    r = requests.get(url, params=payload)
    # 用户发布的帖子数
    media_num = re.findall('"count": (.*?),', r.text)[0]
    payload['first'] = 200
    print('=============================\n' +
          '共找到' + media_num + '张图片、视频\n' +
          '=============================')

    # 帖子数多时分批请求json数据
    r = requests.get(url, params=payload)
    end_cursor = re.findall('"end_cursor": "(.*?)"', r.text)
    payload['after'] = end_cursor
    get_user_image_and_video(re.findall('"node":(.*?)"edge_liked_by"', r.text))
    for index in range(int(int(media_num)/200)):
        r = requests.get(url, params=payload)
        end_cursor = re.findall('"end_cursor": "(.*?)"', r.text)
        payload['after'] = end_cursor
        get_user_image_and_video(re.findall('"node":(.*?)"edge_liked_by"', r.text))


def get_user_image_and_video(data):

    # path = os.getcwd()

    print('start download')

    request_list = []  # 存放任务列表
    fun_var = []
    # 构造任务列表
    for node in data:
        # os.chdir(path)
        if re.findall('GraphImage', node):
            # os.chdir('image')
            fun_var.append((['image', re.findall('"display_url": "(.*?)"', node)[0]], None))
        elif re.findall('GraphSidecar', node):
            # os.chdir('image')
            fun_var.append((['slider', re.findall('"shortcode": "(.*?)"', node)[0]], None))
        elif re.findall('GraphVideo', node):
            # os.chdir('video')
            fun_var.append((['video', re.findall('"shortcode": "(.*?)"', node)], None))

    request_list = threadpool.makeRequests(save, fun_var)
    # map(pool.putRequest, request_list)
    [pool.putRequest(req) for req in request_list]
    # 等待所有任务处理完成，则返回，如果没有处理完，则一直阻塞
    pool.wait()


def save(media_type, code):
    time.sleep(1)
    file_name = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    if media_type == 'image':
        file_name += '.jpg'
        save_image(file_name, code)
    elif media_type == 'video':
        file_name += '.mp4'
        save_video(file_name, code)
    elif media_type == 'slider':
        save_slider(code)


def save_image(file_name, image_url):
    """
    保存照片到本地
    :param username:
    :param image_url:
    :return:
    """

    print('saving image...')
    if image_url:
        pass
    else:
        return
    global headers
    # 新建文件
    file = open(file_name, 'wb')
    # 获取照片
    r = requests.get(image_url, headers=headers, timeout=30)
    file.write(r.content)
    file.close()


def save_video(file_name, shortcode):
    """
    保存视频到本地
    :param username:
    :param shortcode:
    :return:
    """
    print('saving video...')

    if shortcode:
        pass
    else:
        return

    global video_count

    url = 'https://www.instagram.com/p/' + shortcode[0] + '/?__a=1'
    r = requests.get(url, headers=headers)
    video_url = re.findall('"video_url": "(.*?)"', r.text)
    # print('正在下载视频')
    # print(video_url[0])
    r_video = requests.get(video_url[0], headers=headers, timeout=60)
    f = open(file_name, 'wb')
    f.write(r_video.content)
    f.close()


def save_slider(shortcode):
    if shortcode:
        pass
    else:
        return

    url = 'https://www.instagram.com/p/' + shortcode + '/?__a=1'
    r = requests.get(url, headers=headers)
    image_url_list = re.findall('"display_url": "(.*?)"', r.text)
    # 第一张封面和第二张重复
    image_url_list = image_url_list[1:]
    for url in image_url_list:
        file_name = ''.join(random.sample(string.ascii_letters + string.digits, 8)) + '.jpg'
        # threading.Thread(target=save_image, args=(file_name, url)).start()
        save_image(file_name, url)


def main():

    if os.path.exists('download'):
        os.chdir('download')
    else:
        os.mkdir('download')
        os.chdir('download')


    # save_image(get_user_image(sys.argv[1]), sys.argv[1])
    # user_name = sys.argv[1]
    user_name = 'paris_gong'
    download(user_name)
    # print('=============================\n' +
    #       '全部下载完成\n' +
    #       '一共下载了' + str(image_count) + '张图片、' + str(video_count) + '个视频\n' +
    #       '=============================\n')

if __name__ == "__main__":
    main()
