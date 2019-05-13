# -*- coding: utf-8 -*-
import codecs
import time
import requests
import csv

headers = {
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36"
    "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
}

# 通过视频id获取视频的详细信息
def get_detial(list_result):
    for liss in list_result:
        aid = liss[0]  # 视频id
        url_2 = 'https://api.bilibili.com/x/web-interface/view?aid=' + str(aid)  # 视频页面url
        req = requests.get(url_2, headers, timeout=6).json()
        data_ori = req["data"]
        data = data_ori["stat"]
        video = (
            liss[2],  # 标题
            data["aid"],  # 视频号
            data["view"],  # 播放数
            data["danmaku"],  # 弹幕数
            data["reply"],  # 评论数
            data["favorite"],  # 收藏数
            data["coin"],  # 投币数
            data["share"],  # 分享数
            data["like"],  # 点赞数
            data["dislike"],  # 不喜欢数
            liss[1],  # 综合得分
        )
        write_csv(video)  # 将数据写入csv文件中
        print(video)  # 打印写入数据


# 定义排行榜的url
def defined_url1(newarc_type, newday, newrid):
    rid = newrid  # 排行榜分区 id
    day = newday  # 时间跨度
    arc_type = newarc_type  # 投稿时间

    url_1 = "https://api.bilibili.com/x/web-interface/ranking?rid=" + str(rid) + "&day=" + str(
        day) + "&type=1&jsonp=jsonp&arc_type=" + str(arc_type)  # 排行榜url

    return url_1


# 获取视频id
def get_aid(url):
    list_result = []  # 临时存储排行榜页面的数据
    req = requests.get(url, headers=headers, timeout=6).json()
    date_org = req["data"]
    data = date_org["list"]
    for item in data:
        a = item.get('aid', 'NA')
        b = str(item.get('pts', 'NA'))
        c = item.get('title', 'NA')  # 将数据排列
        temp_result = (a, b, c)  # 将数据保存到元组中
        list_result.append(temp_result)  # 将元组中的数据转移到列表中
    get_detial(list_result)  # 通过视频id获取视频详细信息


# 构造一个csv文件
def create_csv():
    with codecs.open("video_stats.csv", "w", "utf-8") as csvfile:
        writer = csv.writer(csvfile)
        # 先写入columns_name
        writer.writerow(
            ["标题", "视频号", "播放数", "弹幕数", "评论数", "收藏数", "投币数", "分享数", "点赞数", "不喜欢数", "综合得分"])
        writer.writerow(
            ["Title", "Aid", "View", "Danmaku", "Reply", "Favorite", "Coin", "Share", "Like", "Dislike", "Pts"])


# 把数据写入csv文件
def write_csv(video):
    with codecs.open("video_stats.csv", "a", "utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows([[video[0], video[2], video[3], video[4], video[5], video[6], video[7], video[8],
                           video[9], video[10], video[1]]])


if __name__ == "__main__":
    create_csv()
    p = 1  # 循环次数
    list_rid = [0, 1, 168, 3, 129, 4, 36, 160, 119, 155, 5, 181]  # 排行榜分区 id
    list_days = [3]  # 时间跨度
    list_arc_type = [1]  # 投稿时间
    for i in list_arc_type:
        for j in list_days:
            for k in list_rid:
                print("这是第" + str(p) + "次")
                get_aid(defined_url1(str(i), str(j), str(k)))
                p += 1
