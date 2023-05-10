import tkinter as tk
import requests
import time
import get
import total
import threading

count_num = 1
playing = False

def on_button_click():
    global playing
    if playing == True:
        return
    # 获取用户输入的参数
    url_prefix = url_entry.get()
    num_chapters = int(num_entry.get())
    retries_time = int(retries_entry.get())

    # 拼接 URL 模板
    # url_template = url_prefix + '{}'

    # 调用 get.py 文件中的代码
    t = threading.Thread(target=get.get_novel, args=(url_prefix, num_chapters, retries_time,updata_progress,init))
    # t.daemon = True  # 将线程 t 设置为守护线程
    print('开始下载')
    t.start()
    playing = True

def on_num_var_changed(*args):
    global count_num
    if not num_var.get():
        # 如果输入为空字符串，则给一个默认值或者抛出错误等处理方式
        count_num = 0  # 给一个默认值
        updata_progress(0)
    else:
        count_num = int(num_var.get())
        updata_progress(0)

    

def get_total_chapters():
    url_prefix = url_entry.get()
    count = total.total(url_prefix) # 调用获取总章节数的函数
    num_var.set(str(count)) # 将获取到的总章节数赋值给num_entry
    global count_num
    count_num = count
    updata_progress(0)

def updata_progress(e):
    global count_num
    progress_label.config(text=f'进度: {e}/{count_num}')

def init():
    global playing
    playing = False


# 全局变量，记录失败次数
failed_attempts = 0

# 检查网站可访问性
def check_website_accessibility(url):
    global failed_attempts

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        status_label.config(text='网络状态：可访问', fg='green')

        # 如果请求成功，重置失败次数
        failed_attempts = 0
    except requests.exceptions.RequestException as e:
        failed_attempts += 1

        # 连续三次失败则标记为不可访问
        if failed_attempts >= 3:
            status_label.config(text='网络状态：不可访问', fg='red')

# 持续检查网站可访问性
def check_website_thread():
    while True:
        check_website_accessibility('https://ncode.syosetu.com/')

# 创建线程并启动
thread = threading.Thread(target=check_website_thread)
thread.start()


# 创建主窗口
root = tk.Tk()
root.title("小说下载")

# 创建画布
canvas = tk.Canvas(root, width=600, height=400)
canvas.pack()

# 创建标签
label = tk.Label(root, text="输入参数，点击按钮开始下载小说", font=('Helvetica', 16))
label.place(relx=0.5, rely=0.1, anchor="center")

status_label = tk.Label(root, text='网络状态：测试中')
status_label.place(relx=0.5, rely=0.23, anchor="center")

# 创建进度标签
progress_label = tk.Label(root, text="进度：0/1")
progress_label.place(relx=0.5, rely=0.3, anchor="center")


# 创建输入框和标签
url_label = tk.Label(root, text="URL前缀：")
url_label.place(relx=0.2, rely=0.4, anchor="center")
url_var = tk.StringVar(value="https://ncode.syosetu.com/n5677cl/")
url_entry = tk.Entry(root, textvariable=url_var)
url_entry.place(relx=0.5, rely=0.4, anchor="center",width=250)

num_label = tk.Label(root, text="下载章节数量：")
num_label.place(relx=0.2, rely=0.5, anchor="center")
num_var = tk.StringVar(value="1")
num_var.trace("w", on_num_var_changed)
num_entry = tk.Entry(root, textvariable=num_var)
num_entry.place(relx=0.5, rely=0.5, anchor="center", width=250)
total_chapters_button = tk.Button(root, text="获取总章节数量", command=get_total_chapters)
total_chapters_button.place(relx=0.8, rely=0.5, anchor="center")

retries_label = tk.Label(root, text="下载出错时重试间隔：")
retries_label.place(relx=0.2, rely=0.6, anchor="center")
retries_var = tk.StringVar(value="5")
retries_entry = tk.Entry(root, textvariable=retries_var)
retries_entry.place(relx=0.5, rely=0.6, anchor="center",width=250)

# 创建按钮
button = tk.Button(root, text="开始下载", padx=10, pady=5, fg="white", bg="#4d4d4d", command=on_button_click)
button.place(relx=0.5, rely=0.8, anchor="center")

# 运行主循环
root.mainloop()
