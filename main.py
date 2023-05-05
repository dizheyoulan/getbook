import tkinter as tk
import get
import total


def on_button_click():
    # 获取用户输入的参数
    url_prefix = url_entry.get()
    num_chapters = int(num_entry.get())
    max_retries = int(retries_entry.get())

    # 拼接 URL 模板
    # url_template = url_prefix + '{}'

    # 调用 get.py 文件中的代码
    get.get_novel(url_prefix, num_chapters, max_retries)

def get_total_chapters():
    url_prefix = url_entry.get()
    count = total.total(url_prefix) # 调用获取总章节数的函数
    num_var.set(str(count)) # 将获取到的总章节数赋值给num_entry


# 创建主窗口
root = tk.Tk()
root.title("小说爬虫")

# 创建画布
canvas = tk.Canvas(root, width=600, height=400)
canvas.pack()

# 创建标签
label = tk.Label(root, text="输入参数，点击按钮开始爬取小说")
label.place(relx=0.5, rely=0.2, anchor="center")

# 创建输入框和标签
url_label = tk.Label(root, text="URL前缀：")
url_label.place(relx=0.2, rely=0.4, anchor="center")
url_var = tk.StringVar(value="https://ncode.syosetu.com/n5677cl/")
url_entry = tk.Entry(root, textvariable=url_var)
url_entry.place(relx=0.5, rely=0.4, anchor="center",width=250)

num_label = tk.Label(root, text="爬取章节数量：")
num_label.place(relx=0.2, rely=0.5, anchor="center")
num_var = tk.StringVar(value="1")
num_entry = tk.Entry(root, textvariable=num_var)
num_entry.place(relx=0.5, rely=0.5, anchor="center",width=250)
total_chapters_button = tk.Button(root, text="获取总章节数量", command=get_total_chapters)
total_chapters_button.place(relx=0.8, rely=0.5, anchor="center")

retries_label = tk.Label(root, text="重试次数：")
retries_label.place(relx=0.2, rely=0.6, anchor="center")
retries_var = tk.StringVar(value="3")
retries_entry = tk.Entry(root, textvariable=retries_var)
retries_entry.place(relx=0.5, rely=0.6, anchor="center",width=250)

# 创建按钮
button = tk.Button(root, text="开始爬取", padx=10, pady=5, fg="white", bg="#4d4d4d", command=on_button_click)
button.place(relx=0.5, rely=0.8, anchor="center")

# 运行主循环
root.mainloop()
