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

# logging 教程待写
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s: %(message)s")

BASE_URL = "https://static1.scrape.center/"
TOTAL_PAGE = 10

# 1
def scrape_page(url):
    """
    考虑到，我们不仅仅要抓取主页面，还需要抓取详情页的数据，所以这个地方，我编写了一个比较通用的爬取页面的方法。
    :param url:
    :return: response.text >>> HTML
    """
    logging.info("scraping %s...", url)
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
        detail_url = urljoin(BASE_URL, href)
        # detail_url = "https://static1.scrape.center" + href # 不推荐
        logging.info("get detail url %s", detail_url)
        yield detail_url

