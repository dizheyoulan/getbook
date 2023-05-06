def get_novel(url_prefix, num_chapters, max_retries,updata_progress,init):
    import requests
    from bs4 import BeautifulSoup
    import time
    import tkinter as tk
    from tkinter import messagebox

    # 构造 URL
    url_template = url_prefix + '{}/'

    # 发送 HTTP 请求并获取响应，设置超时时间为5秒钟
    for retry in range(max_retries):
        try:
            # 定义请求头信息
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }

            # 发送 HTTP 请求并获取响应，设置超时时间为5秒钟
            response = requests.get(url_template.format(1), headers=headers, timeout=5)

            # 如果请求失败，等待5秒钟后重试
            if response.status_code != 200:
                print(f'请求失败 status为 {response.status_code}, 5秒钟后重试...')
                time.sleep(5)
                continue

            # 将响应中的 HTML 数据解析为 BeautifulSoup 对象
            soup = BeautifulSoup(response.content, 'html.parser')

            # 获取小说书名
            name = soup.select_one('.contents1 a').text.strip()

            # 获取小说作者
            author = soup.select_one('.contents1 a[href^="https://mypage.syosetu.com/"]').text.strip()

            # 写入书名和作者名
            with open(f'{name}.txt', 'w', encoding='utf-8') as f:
                f.write(f'书名：{name}\n')
                f.write(f'作者：{author}\n')

            # 跳出重试循环
            break

        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            # 如果出现网络超时或连接错误，等待5秒钟后重试
            print(f'网络超时: {e}, 5秒钟后重试...')
            time.sleep(5)
            continue

        except Exception as e:
            # 如果出现其他异常，打印异常信息并退出程序
            print(f'其他异常: {e}')
            exit()

    # 遍历章节列表，并依次访问每个URL
    for i in range(1, num_chapters+1):
        # 构造当前章节的URL
        url = url_template.format(i)

        for retry in range(max_retries):
            try:
                # 发送 HTTP 请求并获取响应，设置超时时间为5秒钟
                response = requests.get(url, headers=headers, timeout=5)

                # 如果请求失败，等待5秒钟后重试
                if response.status_code != 200:
                    print(f'请求失败 status为 {response.status_code}, 5秒钟后重试...')
                    time.sleep(5)
                    continue

                # 将响应中的 HTML 数据解析为 BeautifulSoup 对象
                soup = BeautifulSoup(response.content, 'html.parser')

                # 获取小说标题
                title = soup.select_one('.novel_subtitle').text.strip()

                # 获取小说章节内容
                content = soup.select_one('#novel_honbun').text.strip()

                # 将结果写入到txt文件
                with open(f'{name}.txt', 'a', encoding='utf-8') as f:
                    f.write(f'第{i}章 {title}\n\n{content}\n\n\n')
                    updata_progress(i)
                    if num_chapters == i:
                        messagebox.showinfo('提示', '下载完成！')
                        init()

                # 跳出重试循环
                break

            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                # 如果出现网络超时或连接错误，等待5秒钟后重试
                print(f'网络超时: {e}, 5秒钟后重试...')
                time.sleep(5)
                continue

            except Exception as e:
                # 如果出现其他异常，打印异常信息并退出程序
                print(f'其他异常: {e}')
                exit()
