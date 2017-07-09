# Instagram_Spider

根据用户名自动下载Instagram上用户的所有图片、视频

## Run

python3 main.py username

## 依赖模块

1. requests(2.8.1)
2. threadpool(1.3.2)

## 一些Instagram API

1. 返回用户帖子数据

`https://www.instagram.com/graphql/query/?query_id=17862015703145017&id=480496199&first=5&after=AQDlUE2N2oLDDxlocVzAX-ot8tj7FG63Rssv3QJb8Kzxvn75gjsOHgjjNKx_QI-paHgWfTAaTC_dn47sgBUuAu0QD6kVpUS0soSV5DbKppXuNg`

- query_id: 不知道干嘛的
- id: 用户id
- first: 返回数据的数量
- after: 从某一个帖子开始

```JSON
{
  "data": {
    "user": {
      "edge_owner_to_timeline_media": {
        "count": 656,
        "page_info": {
          "has_next_page": true,
          // end_cursor: 此json数据中最后一条帖子的编号
          "end_cursor": "AQByoKgYVItwT0NPxVuBa5euRx-yP9crjfKPyoPfLiQrU2sqOpvLTo0aT-JCqYJ2LK77NfR_3jN-qxe2QgQqJJLstp_e1AFU7V3rhsVR8oX-wQ"
        },
        "edges": [
          {
            "node": {
              "id": "1554427407196635596",
              // 帖子类型
              "__typename": "GraphImage",
              "edge_media_to_caption": {
                "edges": [
                  {
                    "node": {
                      "text": "#Vans\n有点GayGay的"
                    }
                  }
                ]
              },
              "shortcode": "BWSb327FkHM",
              "edge_media_to_comment": {
                "count": 9
              },
              "comments_disabled": false,
              "taken_at_timestamp": 1499522208,
              "dimensions": {
                "height": 1080,
                "width": 1080
              },
              // 高清图url
              "display_url": "https://scontent-sjc2-1.cdninstagram.com/t51.2885-15/e35/19764838_425459937852869_7328132977790025728_n.jpg",
              "edge_liked_by": {
                "count": 6
              },
              "owner": {
                "id": "480496199"
              },
              "thumbnail_src": "https://scontent-sjc2-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/19764838_425459937852869_7328132977790025728_n.jpg",
              "thumbnail_resources": [],
              "is_video": false
            }
          }
        ]
      }
    }
  },
  "status": "ok"
}
```

2. 返回用户视频数据

`https://www.instagram.com/p/{shortcode}/?__a=1`