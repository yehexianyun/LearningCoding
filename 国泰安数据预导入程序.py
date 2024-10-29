*-*- coding: utf-8 -*-
"""
该文件代码的目标是将国泰安的数据完整地导入stata，将标签作为标签导入，将数据来源中作为注释导入。以下代码可结合后台自动执行python代码的程序进行自动化处理。
"""
#为控制台运行的Python代码加入参数
import sys

if __name__ == "__main__":
    # 获取命令行参数
    folderpath = sys.argv[1]
    
    # 在这里可以使用 folder 变量进行操作
    print("Folder:", folderpath)

#%%环境准备
import stata_setup
stata_setup.config(r"C:\Program Files\Stata18", "mp")
from pystata import stata
import os
#%%文件获取
#获取文件夹中的csv文件
files = os.listdir(folderpath)
files = [file for file in files if file.endswith(".csv")]
#去掉扩展名
filename = files[0].split(".")[0]
#获取文件夹中的txt文件
txtfiles = os.listdir(folderpath)
txtfiles = [file for file in txtfiles if file.endswith(".txt")]
csvfile = folderpath+"\\"+files[0]
txtfile = folderpath+"\\"+txtfiles[0]
f = open(txtfile, "r",encoding='utf-8')
lines = f.readlines()
f.close()
#%%运行导入程序
variablename = [line[:line.index("[")] for line in lines]
variablename = [var.lower() for var in variablename]
variablelabel = [line[line.index("[")+1:line.index("]")] for line in lines]
variablenote = [line[line.index("]")+1:] for line in lines]

stata.run("import delimited " +'"'+ csvfile + '"'+ ",varnames(1) clear")
for var in variablename:
    stata.run("label variable " + var + ' "' + variablelabel[variablename.index(var)] + '"')
    stata.run("notes "+ var + ":" + variablenote[variablename.index(var)])
stata.run("save " + filename + ".dta, replace")
