import pandas as pd
import jieba
jieba.load_userdict('E:\\论文工作区\\MacroCognition\\CMDA_管理层讨论与分析_ALL\\用户词表2.txt')
data = pd.read_excel("E:\\论文工作区\\MacroCognition\\CMDA_管理层讨论与分析_ALL\\2022.xlsx")
#将Enddate列转换为日期格式
data['Enddate'] = pd.to_datetime(data['Enddate'])
#提取年份
data['year'] = data['Enddate'].dt.year
#提取月份
data['month'] = data['Enddate'].dt.month
#只保留月份为12的行
data = data[data['month'] == 12]
with open("E:\\论文工作区\\MacroCognition\\CMDA_管理层讨论与分析_ALL\\宏观经济感知词表.txt",'r',encoding='utf-8') as f:
    macro_word = f.read()
    macro_word_list = macro_word.split('\n')
with open("E:\\论文工作区\\MacroCognition\\CMDA_管理层讨论与分析_ALL\\积极词汇.txt",'r',encoding='utf-8') as f:
    pos_word = f.read()
    pos_word_list = pos_word.split('\n')

with open("E:\\论文工作区\\MacroCognition\\CMDA_管理层讨论与分析_ALL\\消极词汇.txt",'r',encoding='utf-8') as f:
    neg_word = f.read()
    neg_word_list = neg_word.split('\n')
#重建索引
data = data.reset_index()
#新建一列MacroSense
data['MacroSense'] = 0
#对data的ManaDiscAnal列每一行进行循环
#i从1开始
#j从0开始

for i in range(1,len(data)):
    #提取每一行的ManaDiscAnal列
    text = data['ManaDiscAnal'][i]

    macro_index_list = list()
    text = text.replace('\n', '')
    text_list = text.split('。')
    macro_sense = list(range(len(text_list))) #初始化宏观指数
    for j in range(len(text_list)):
        word_list = jieba.lcut(text_list[j])
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
            macro_sense[j] = 1
        elif macro_index < 0:
            macro_sense[j] = -1
        else:
            macro_sense[j] = 0
    macro_sense_num = sum(macro_sense)
    data["MacroSense"][i] = macro_sense_num
    pass

#删除ManaDiscAnal列
data = data.drop(['ManaDiscAnal'],axis = 1)
data.to_csv("E:\\论文工作区\\MacroCognition\\data.csv",encoding = 'gbk')