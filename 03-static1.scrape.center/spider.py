# -*- coding: utf-8 -*-
# @Time    : 2022/5/22 21:59
# @Author  : AI悦创
# @FileName: spider.py
# @Software: PyCharm
# @Blog    ：https://bornforthis.cn/
# 多进程、requests、regx、pyquery、PymongoDB
"""
1. requests 爬取这个站点每一页的电影列表，顺着列表再爬取每个电影详情页；
1. Crawls the list of movies on each page of the site, and then crawls down the list to each movie detail page.
2. 用 pyquery 和正则表达式提取每部电影的名称、封面、类别、上映时间、评分、剧情简介等内容；
2. Use pyquery and regular expressions to extract the name, cover, category, release date, rating, synopsis, and so on of each movie.
3. 以上爬取的内容，存入 MongoDB；
3. The contents of the crawled above are stored in MongoDB;
4. 使用多进程实现爬取加速。
4. Climbing acceleration using multiple processes.
-------------------------------------------------
"""

"""
如果我们要完成列表页的爬取，可以如下实现：
- 遍历页码构造 10页索引 URL
- 从每个索引页分析提取出每个电影的详情页 URL
"""
import requests  # 爬取页面
import logging  # logging 用来输出信息
import re  # re 用来实现正则表达式解析
import pymongo  # 用来数据存储
from pyquery import PyQuery as pq  # 用来直接解析网页
from urllib.parse import urljoin  # 用来 URL 的拼接
from inster_data_function import write_mongodb

# --------
# from bs4 import BeautifulSoup

CLIENT = pymongo.MongoClient(host="localhost", port=27017)
db = CLIENT["Movies"]
collection = db["Movies"]

# logging 教程待写
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s: %(message)s")

BASE_URL = "https://static1.scrape.center"
TOTAL_PAGE = 10


# 1
def scrape_page(url):
    """
    考虑到，我们不仅仅要抓取主页面，还需要抓取详情页的数据，所以这个地方，我编写了一个比较通用的爬取页面的方法。
    :param url:
    :return: response.text >>> HTML
    """
    # logging.info("scraping %s...", url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        logging.error("get invalid status code %s while scraping %s", response.status_code, url)
    except requests.RequestException:
        logging.error("error occurred while scraping %s", url, exc_info=True)


# 2
def scrape_index(page):
    index_url = f"{BASE_URL}/page/{page}"  # 构造链接
    return scrape_page(index_url)  # 直接取抓取


# 3
def parse_index(html):
    doc = pq(html)
    links = doc(".el-card .name")
    for link in links.items():
        href = link.attr("href")
        # print("href:", href)
        detail_url = urljoin(BASE_URL, href)
        # detail_url = "https://static1.scrape.center" + href # 不推荐
        # logging.info("get detail url %s", detail_url)
        yield detail_url


# 4 请求详情页
def scrape_details(url):
    return scrape_page(url)


def parse_details(html):
    # soup = BeautifulSoup(html, "lxml")
    # img_link = soup.select(".el-col .cover")
    #
    # print(img_link)
    doc = pq(html)
    # 1. 电影图片
    img_cover = doc('img.cover').attr("src")
    # 2. 电影名称
    # name = doc("a h2")
    name = doc("a > h2").text()
    # 3. 电影标签
    categories = [item.text() for item in doc(".categories button span").items()]
    # 4. 上映时间
    # published_at = [item.text() for item in doc(".info span").items()]
    # published_at = "".join(published_at)
    published_at = doc(".info:contains(上映)").text()
    # 1993-07-26 上映
    # re
    published_at = re.search('(\d{4}-\d{2}-\d{2})', published_at).group(1) \
        if published_at and re.search('\d{4}-\d{2}-\d{2}', published_at) else None
    # 与上面的代码等价
    # if published_at and re.search('\d{4}-\d{2}-\d{2}', published_at):
    #     published_at = re.search('(\d{4}-\d{2}-\d{2})', published_at).group(1)
    # else:
    #     published_at = None
    # 5. 剧情简介
    drama = doc(".drama p").text()
    # 6. 评分
    score = doc("p.score").text()
    # 转换数据类型
    # if score:
    #     score = float(score)
    # else:
    #     score = None
    score = float(score) if score else None
    # print(img_cover)
    # print(name)
    # print(categories, type(categories))
    # print(published_at)
    # print(drama)
    # print(score)
    return {
        "img_cover": img_cover,
        "name": name,
        "categories": categories,
        "published_at": published_at,
        "drama": drama,
        "score": score,
    }


def save_data(data):
    collection.update_one({
        'name': data.get('name'),
    }, {
        '$set': data
    }, upsert=True)

def save_data_two(data):
    write_mongodb(
        db_name="Movie_two",
        table_name="Movie_two",
        insert_data=data
    )

def main():
    for page in range(1, TOTAL_PAGE + 1):
        index_html = scrape_index(page)
        detail_urls = parse_index(index_html)
        # logging.info("detail urls %s", list(detail_urls)
        for url in detail_urls:
            html = scrape_details(url)
            data = parse_details(html)
            print(data)
            save_data(data)
            save_data_two(data)



if __name__ == '__main__':
    main()
