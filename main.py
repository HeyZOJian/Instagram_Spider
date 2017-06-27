import requests
import re
import os
import sys

# 记录下载视频数
video_count = 0
# 记录下载图片数
image_count = 0

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
    return (re.findall('"owner": {"id": "(.*?)"},', text)[0],
            re.findall('<meta property="og:description" content=".* Following, (.*?) Posts', text)[0])


def get_user_data(username):
    """
    获取用户所有的照片和视频json信息
    :param username:
    :return:
    """

    user_id, media_num = get_user_info(username)

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


def get_user_image_and_video(username):
    global image_count
    global video_count

    if os.path.exists(username):
        os.chdir(username)
    else:
        os.mkdir(username)
        os.chdir(username)

    path = os.getcwd()
    data = get_user_data(username)
    for node in data:
        os.chdir(path)
        if re.findall('GraphImage', node):
            print('正在下载图片')
            image_count += 1
            # print('url:' + str(re.findall('"display_url": "(.*?)"', node)))
            save_image(username, re.findall('"display_url": "(.*?)"', node))
        elif re.findall('GraphSidecar', node):
            # 多张图片
            pass
        elif re.findall('GraphVideo', node):
            print('正在下载视频')
            video_count += 1
            # FIXME: 有些shortcode找不到
            save_video(username, re.findall('"shortcode": "(.*?)"', node))


def save_image(username, image_url):
    """
    保存照片到本地
    :param username:
    :param image_url:
    :return:
    """

    os.chdir('image')

    if image_url:
        pass
    else:
        return

    image_url = image_url[0]

    global headers
    global image_count

    print(image_url)
    # 由url生成照片文件名
    image_filename = username + '_' + str(image_count) + '.jpg'
    # 新建文件
    file = open(image_filename, 'wb')
    # 获取照片
    r = requests.get(image_url, headers=headers, timeout=30)
    # FIXME: 保存的照片都是正方形
    file.write(r.content)
    file.close()


def save_video(username, shortcode):
    """
    保存视频到本地
    :param username:
    :param shortcode:
    :return:
    """

    os.chdir('video')

    global video_count
    if shortcode:
        pass
    else:
        return
    url = 'https://www.instagram.com/p/' + shortcode[0] + '/?__a=1'
    r = requests.get(url, headers=headers)
    video_url = re.findall('"video_url": "(.*?)"', r.text)
    print(video_url[0])
    r_video = requests.get(video_url[0], headers=headers, timeout=60)
    video_filename = username + '_' + str(video_count) + '.mp4'
    f = open(video_filename, 'wb')
    f.write(r_video.content)
    f.close()


def main():

    if os.path.exists('download'):
        os.chdir('download')
    else:
        os.mkdir('download')
        os.chdir('download')

    # save_image(get_user_image(sys.argv[1]), sys.argv[1])

    get_user_image_and_video(sys.argv[1])
    print('=============================\n' +
          '全部下载完成\n' +
          '一共下载了' + str(image_count) + '张图片、' + str(video_count) + '个视频\n' +
          '=============================\n')


if __name__ == "__main__":
    main()

# FIXME: 爬到一定时间出现错误：
# requests.exceptions.ConnectionError: HTTPSConnectionPool(host='ig-s-c-a.akamaihd.net', port=443): Read timed out.
# FIXME: 有些视频和图片爬不到