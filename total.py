import requests
from bs4 import BeautifulSoup
import time

def total(url_prefix):
    # 定义请求头信息
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    while True:
        try:
            # 发送 HTTP 请求并获取响应，设置超时时间为5秒钟
            response = requests.get(url_prefix, headers=headers, timeout=5)
            # 如果请求成功，退出循环
            if response.status_code == 200:
                break
            # 如果请求失败，等待5秒钟后重试
            print(f'请求失败 status为 {response.status_code}, 5秒钟后重试...')
            time.sleep(5)
        except:
            # 如果请求异常，等待5秒钟后重试
            print('请求异常，5秒钟后重试...')
            time.sleep(5)

    # 将响应中的 HTML 数据解析为 BeautifulSoup 对象
    soup = BeautifulSoup(response.content, 'html.parser')

    # 找到最后一章的标签
    last_chapter_tag = soup.select('.novel_sublist2')[-1]

    # 从标签中提取章节号
    latest_chapter = last_chapter_tag.select_one('.novel_sublist2 dd.subtitle a')['href'].split('/')[-2]
    print(f'章节总数: {latest_chapter}')
    return latest_chapter