# sourcery skip: remove-redundant-pass
import pandas as pd
import numpy as np
import os
import jieba
# 指定文件夹路径
year = input("输入年份:")
folder_path = "E:\\论文工作区\\MacroCognition\\CMDA_管理层讨论与分析_ALL\\"+year+"\\文本\\文本"

jieba.load_userdict('E:\\论文工作区\\MacroCognition\\CMDA_管理层讨论与分析_ALL\\用户词典.txt')
# 获取文件夹中所有文件名
data = pd.DataFrame()
data['code'] = []
file_names = os.listdir(folder_path)
data['path'] = file_names
data['code'] = data['path'].apply(lambda x: x[:6])
data['date'] = data['path'].apply(lambda x: x[7:17])
data.loc[:,'macro_index'] = ""
data.drop
with open("E:\\论文工作区\\MacroCognition\\CMDA_管理层讨论与分析_ALL\\宏观词汇表2.txt",'r',encoding='utf-8') as f:
    macro_word = f.read()
    macro_word_list = macro_word.split('\n')
with open("E:\\论文工作区\\MacroCognition\\CMDA_管理层讨论与分析_ALL\\积极词汇.txt",'r',encoding='utf-8') as f:
    pos_word = f.read()
    pos_word_list = pos_word.split('\n')

with open("E:\\论文工作区\\MacroCognition\\CMDA_管理层讨论与分析_ALL\\消极词汇.txt",'r',encoding='utf-8') as f:
    neg_word = f.read()
    neg_word_list = neg_word.split('\n')

macro_index_list = list()
#分句
for file_name in os.listdir(folder_path):
    if file_name.endswith('.txt'):
        with open(os.path.join(folder_path, file_name), 'r',encoding = 'utf-8') as f:
            # 在这里进行文件操作
            text = f.read()
            a =  0
            text = text.replace('\n', '')
            text_list = text.split('。')
            macro_sense = list(range(len(text_list)))
            for i in range(len(text_list)):
                word_list = jieba.lcut(text_list[i])
                x = 0
                y = 0
                z = 0
                for word in word_list:
                    if word in macro_word_list:
                        x = x + 1
                if x > 0:
                    if word in pos_word_list:
                        y += 1
                    elif word in neg_word_list:
                        z += 1
                else:
                    pass
                macro_index = (y - z) * x
                if macro_index > 0:
                    macro_sense[i] = 1
                elif macro_index < 0:
                    macro_sense[i] = -1
                else:
                    macro_sense[i] = 0
            macro_sense_num = sum(macro_sense)
            macro_index_list = macro_index_list + [macro_sense_num]
            #df = data[['code','macro_index']]
            #df.loc[8484]['macro_index'] = macro_sense_num
            pass
data['macro_index'] = macro_index_list
data.to_csv('E:\\论文工作区\\MacroCognition\\CMDA_管理层讨论与分析_ALL\\宏观指数'+year+'.csv',encoding = 'utf-8-sig')     

