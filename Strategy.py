#%%数据导入
import pandas as pd
import numpy as np
import talib
import feather
data = feather.read_dataframe('D:/Stock/data.feather')
# %%预处理
#列所有列名称
print(data.columns.tolist())
# 保留列
data = data[["股票代码_Stkcd","日期_Date",'前收盘价_PrevClPr','开盘价_Oppr', '最高价_Hipr', '最低价_Lopr', '收盘价_Clpr','成交量_Trdvol','日收益率_Dret','日振幅(%)_Dampltd']]
#将'前收盘价_PrevClPr','开盘价_Oppr', '最高价_Hipr', '最低价_Lopr', '收盘价_Clpr','成交量_Trdvol','日收益率_Dret','日振幅(%)_Dampltd'转换为float
data["前收盘价_PrevClPr"] = data["前收盘价_PrevClPr"].astype(float)
data["开盘价_Oppr"] = data["开盘价_Oppr"].astype(float)
data["最高价_Hipr"] = data["最高价_Hipr"].astype(float)
data["最低价_Lopr"] = data["最低价_Lopr"].astype(float)
data["收盘价_Clpr"] = data["收盘价_Clpr"].astype(float)
data["成交量_Trdvol"] = data["成交量_Trdvol"].astype(float)
data["日收益率_Dret"] = data["日收益率_Dret"].astype(float)
data["日振幅(%)_Dampltd"] = data["日振幅(%)_Dampltd"].astype(float)

# %%指标计算
# 上涨下跌分类
data['Updown'] = data['日收益率_Dret']> 0
# 按照股票代码_Stkcd分组计算MA60
data.sort_values(['股票代码_Stkcd', '日期_Date'], inplace=True)
data['MA60'] = data.groupby('股票代码_Stkcd')['收盘价_Clpr'].transform(lambda x: talib.MA(x, 60))
# 按照股票代码_Stkcd分组计算MA60的变化率
data['MA60_pct_change'] = data.groupby('股票代码_Stkcd')['MA60'].pct_change(fill_method=None)
data['MA60up'] = data['MA60_pct_change'] > 0
#计算成交量增长率
data['VOL_pct_change'] = data.groupby('股票代码_Stkcd')['成交量_Trdvol'].pct_change(fill_method=None)
data['VOLup'] = data['VOL_pct_change'] > 0
#定义放量上涨
data['Up'] = data['Updown']  & data['VOLup']
#定义缩量下跌
data['Down'] = ~data['Updown'] & ~data['VOLup']

# %%策略

#%%测试
