import requests
import re
import os
import sys


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


def get_user_media(username):
    """
    根据用户名获取用户所有图片的链接
    :param username: 用户名
    :return: 图片链接列表
    """
    user_id, media_num = get_user_info(username)

    print('=============================\n' +
          '共找到'+media_num+'张图片、视频\n' +
          '=============================')

    url = 'https://www.instagram.com/graphql/query/'

    payload = {'query_id': 17880160963012870,
               'id': user_id,
               'first': media_num}

    r = requests.get(url, params=payload)
    return re.findall('"thumbnail_src": "(.*?)",', r.text)


def save_image(list_image, username):
    """
    保存照片到本地
    :param list_image:
    :return:
    """

    header = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, sdch, br'
    }

    if os.path.exists(username):
        os.chdir(username)
    else:
        os.mkdir(username)
        os.chdir(username)

    num = 1

    for url in list_image:
        new_url = re.findall('http.*?/t51.2885-15/', url)[0] + re.findall('/e.*?/(.*?.jpg)', url)[0]

        print('正在下载第:'+str(num)+'张图片')

        num += 1

        file_name = re.findall('t51.2885-15/(.*)', new_url)

        print('文件名：'+file_name[0].replace("/", "_"))

        file = open(file_name[0].replace("/", "_"), 'wb')

        # FIXME: 爬到一定实现出现错误：requests.exceptions.ConnectionError: HTTPSConnectionPool(host='ig-s-c-a.akamaihd.net', port=443): Read timed out.

        r = requests.get(new_url, headers=header, timeout=5)

        # FIXME: 保存的照片都是正方形

        file.write(r.content)
        file.close()
        print('下载成功')


def main():

    if os.path.exists('download'):
        os.chdir('download')
    else:
        os.mkdir('download')
        os.chdir('download')

    save_image(get_user_media(sys.argv[1]), sys.argv[1])

    print('=============================\n' +
          '全部下载完成\n'
          '=============================\n' +)


if __name__ == "__main__":
    main()
