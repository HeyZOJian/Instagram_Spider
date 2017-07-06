import requests
import re
import os
import sys
import threading
import random
import string


headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, sdch, br'
    }


def get_user_info(username):
    """
    获取用户ID和他的帖子数
    :param username: 用户名
    :return: [用户ID，帖子数]
    """
    url = 'https://www.instagram.com/' + username
    text = requests.get(url).text
    try:
        return (re.findall('"owner": {"id": "(.*?)"},', text)[0],
            re.findall('<meta property="og:description" content=".* Following, (.*?) Posts', text)[0])
    except :
        print('找不到该用户')


def get_user_data(user_id, media_num):
    """
    获取用户所有的照片和视频json信息
    :param username:
    :return:
    """

    print('=============================\n' +
          '共找到' + media_num + '张图片、视频\n' +
          '=============================')

    url = 'https://www.instagram.com/graphql/query/'

    payload = {'query_id': 17880160963012870,
               'id': user_id,
               'first': media_num}

    r = requests.get(url, params=payload)

    # f = open('json.txt', 'w')
    # f.write(str(re.findall('"node":(.*?)"edge_liked_by"', r.text)))

    return re.findall('"node":(.*?)"edge_liked_by"', r.text)


def get_user_image_and_video(data, username):
    global image_count
    global video_count

    if os.path.exists(username):
        os.chdir(username)
    else:
        os.mkdir(username)
        os.chdir(username)
        os.mkdir('image')
        os.mkdir('video')

    path = os.getcwd()

    for node in data:
        os.chdir(path)
        if re.findall('GraphImage', node):
            os.chdir('image')
            file_name = ''.join(random.sample(string.ascii_letters + string.digits, 8)) + '.jpg'
            threading.Thread(target=save_image,
                             args=(file_name, re.findall('"display_url": "(.*?)"', node)[0])).start()
        elif re.findall('GraphSidecar', node):
            os.chdir('image')
            threading.Thread(target=save_slider,
                             args=(re.findall('"shortcode": "(.*?)"', node))).start()
        elif re.findall('GraphVideo', node):
            os.chdir('video')
            file_name = ''.join(random.sample(string.ascii_letters + string.digits, 8)) + '.mp4'
            threading.Thread(target=save_video,
                             args=(file_name, re.findall('"shortcode": "(.*?)"', node))).start()


def save_image(file_name, image_url):
    """
    保存照片到本地
    :param username:
    :param image_url:
    :return:
    """

    if image_url:
        pass
    else:
        return

    # image_url = image_url[0]

    global headers
    global image_count
    # print('正在下载图片')
    # print(image_url)
    # 新建文件
    file = open(file_name, 'wb')
    # 获取照片
    r = requests.get(image_url, headers=headers, timeout=30)
    # FIXME: 保存的照片都是正方形
    file.write(r.content)
    file.close()


def save_video(file_name, shortcode):
    """
    保存视频到本地
    :param username:
    :param shortcode:
    :return:
    """
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
    # username = sys.argv[1]
    username = 'zojian'
    user_id, media_num = get_user_info(username)
    if user_id == None:
        return
    data = get_user_data(user_id, media_num)
    get_user_image_and_video(data, username)
    # print('=============================\n' +
    #       '全部下载完成\n' +
    #       '一共下载了' + str(image_count) + '张图片、' + str(video_count) + '个视频\n' +
    #       '=============================\n')

if __name__ == "__main__":
    main()

# FIXME: 出现requests.exceptions.ConnectionError: HTTPSConnectionPool(host='ig-s-b-a.akamaihd.net', port=443): Read timed out.