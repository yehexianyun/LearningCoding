import os
progress = "<progress value=20 max=100></progress>"
def find_markdown_files_in_folders(folders):
    markdown_files = []

    for folder in folders:
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.endswith('.md'):
                    markdown_files.append(os.path.join(root, file))

    return markdown_files

# 设置要搜索的文件夹列表
folders = [
"F:/Knowledge/assets",
"F:/Knowledge/Coding",
"F:/Knowledge/DeepLearning",
"F:/Knowledge/Design",
"F:/Knowledge/Economics",
"F:/Knowledge/Economitrics",
"F:/Knowledge/Finance",
"F:/Knowledge/Inbox",
"F:/Knowledge/KnowledgeManage",
"F:/Knowledge/MachineLearning",
"F:/Knowledge/MATLAB",
"F:/Knowledge/Psychology",
"F:/Knowledge/Python",
"F:/Knowledge/Research",
"F:/Knowledge/Technology",
"F:/Knowledge/TheLife",


]
# 调用函数并打印结果
markdown_files_list = find_markdown_files_in_folders(folders)

marker="#阅读标记"
from typing import List
import os

def analyze_markdown(file_path):
    total_lines = 0
    line_numbers = []

    with open(file_path, 'r', encoding='utf-8') as file:
         for i, line in enumerate(file, 1):
            total_lines += 1 # 从1开始计数
            if marker in line:
                line_numbers.append(i) 
            else:
                line_numbers.append(0) # 添加行号到列表中
    try:
        max_num = max(line_numbers)
    except ValueError:
        max_num = 0
    return total_lines, max_num

import pandas as pd
data = pd.DataFrame()
total_list = [analyze_markdown(file_path) for file_path in markdown_files_list]
#提取markdown_files_list 中的文件名称
filename =[os.path.basename(file_path) for file_path in markdown_files_list]
#将filename中的文件名去除后缀
filename = [os.path.splitext(filename[i])[0] for i in range(len(filename))]
#对filename的每一项前后加上[[和]]
filename = [f"[[{filename[i]}]]" for i in range(len(filename))]
data["Name"] = filename
#新建一个列表
progress_list = []
#将line_numbers中的数字转化为字符串
for i in range(len(total_list)):
    progress_list.append(str(total_list[i][1]))
    progress_list[i] = "<progress value=" + progress_list[i] + " max=" + str(total_list[i][0]) + "></progress>"

data["Progress"] = progress_list

#将data输出为markdown文件。
data.to_markdown("F:/Knowledge/Kanban.md", index=False)

