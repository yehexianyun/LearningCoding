import pandas as pd
import numpy as np
data = pd.read_csv("E:\\论文工作区\\DataOpen\\DailyFileAll\\DailyFile_1996_2022.csv")

statebond = pd.read_csv("E:\\论文工作区\\DataOpen\\Statebond.csv")
#删除statebond中Cvtype值为2的行
statebond = statebond[statebond.Cvtype != 2]
#将data与statebond按照Trddt和Yeartomatu两个条件匹配
data['Trddt'] = pd.to_datetime(data['Trddt'])
#删除data中的Trddt在2017年之前的数据
data = data[data['Trddt'] >= '2017-01-01']
statebond['Trddt'] = pd.to_datetime(statebond['Trddt'])
#删除Yeartomatu为空的行
data = data.dropna(subset=['Yeartomatu'])
#将data的Yeartomatu保留两位小数
data['Yeartomatu'] = data['Yeartomatu'].round(decimals=1)
#将statebond的Yeartomatu保留两位小数
statebond['Yeartomatu'] = statebond['Yeartomatu'].round(decimals=1)
#按照Trddth进行匹配
data = pd.merge(data,statebond,how='left',on=['Trddt','Yeartomatu'])
data['spread'] = data['Yldtomtu'] - data['Yield']
#统计spread的空值数量
data['spread'].isnull().sum()
data = data.dropna(subset=['spread'])
data['year'] = data['Trddt'].dt.year
data  = data.groupby(['Liscd','Sctcd','year'])['spread'].mean()
data = data.reset_index()
bond_info = pd.read_csv("G:\\12_Database\\Bond\\BND_Bndinfo.csv")
spread = pd.merge(data,bond_info,how='left',on=['Liscd','Sctcd'])
#删除重复行
#保留Bndtype为2或3的数据
spread = spread[(spread['Bndtype']==2)|(spread['Bndtype']==3)]
spread = spread.drop_duplicates(['Liscd','Sctcd','year'])
spread.to_csv("E:\\论文工作区\\DataOpen\\spread.csv",index=False,encoding='utf-8-sig')