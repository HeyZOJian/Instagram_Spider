import requests
import re
import os


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


def save_image(list_image):
    """
    保存照片到本地
    :param list_image:
    :return:
    """



    for url in list_image:
        # new_url = re.findall('http.*?/t51.2885-15/', url)[0] + re.findall('/e.*?/(.*?.jpg)', url)[0]

        print('正在下载:'+url)

        file_name = re.findall('t51.2885-15/(.*)', url)

        print('文件名：'+file_name[0].replace("/", "_"))

        file = open(file_name[0].replace("/", "_"), 'wb')

        r = requests.get(url, timeout=5)

        print('打开成功 ！')

        file.write(r.content)
        file.close()
        # print(file_name[0].replace("/", "_")+'download success!')


def main():
    # print(get_user_media('zojian'))
    save_image(get_user_media('zojian'))

if __name__ == "__main__":
    main()
