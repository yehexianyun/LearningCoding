# 编程建议
#1. 导入模块中的部分，而不是全部
from math import sqrt
#2. 使用PEP 8标准
#PEP 8是Python官方的编码风格指南，它为Python程序员提供了代码编写的指导方针，主要介绍Python代码的编写规范，是一种编码风格。
#3. 使用日志输出
import logging
logging.debug('debug message')
#4. 深拷贝与浅拷贝
import pandas as pd
data = pd.read_csv("E:\\论文工作区\\DataOpen\\DailyFileAll\\DailyFile_1996_2022.csv")
data2 = data.copy() # 深拷贝,两个变量指向不同对象,修改data2不会影响data
data3 = data # 浅拷贝，两个变量指向相同对象，修改data3会影响data
#5. 计数器变量
for i ,item in enumerate(list):
    print(i,item)
