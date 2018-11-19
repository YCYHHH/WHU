# Fama Frnech Three Factors Model

# Authors: 肥肠有趣组
# Date: 11/8/2018


# 倒入需要使用的包
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import statsmodels.api as sm


# 从CSMAR数据库下载的2000年到2018年，周频率的三因子数据
data = pd.read_excel(r'weekly_data.xlsx')
# 我们选用A股市场的数据进行本次研究
data = data[data['MarkettypeID'] == 'P9707'].iloc[:, 1:]
# 将原始的数据的日期转换为 int 型方便排序
for i in range(len(data)):
    data.iloc[i, 0] = data.iloc[i, 0].replace('-', '')

# 进行排序，日期采用年份加周数的格式，如：200024表示2000年第24周
data = data.sort_values(axis=0, ascending=True, by='TradingWeek')
# 观察可知里面存在缺失值，因此，我选择进行填补，一年有52周
date = []
for i in range(2000, 2018):
    for j in range(1, 53):
        week = str(i) + str(j).zfill(2)
        date.append(week)
# 2018年一共值39周有数据
for i in range(1, 40):
    week = '2018' + str(i).zfill(2)
    date.append(week)
# 将date转换为DataFrame的格式，方便之后的数据清理
all_time = pd.DataFrame()
all_time['TradingWeek'] = date
# 按照流通市值加权和总市值加权分成2组数据集,fluent_market_value/total_market_value
fmv = data.iloc[:, [0, 1, 3, 5]]  # data1按照流通市值加权
tmv = data.iloc[:, [0, 2, 4, 6]]  # data2按照总市值加权
fmv = pd.merge(all_time, fmv, on='TradingWeek', how='outer')
tmv = pd.merge(all_time, tmv, on='TradingWeek', how='outer')
fmv = fmv.rename(columns={'RiskPremium1': 'RiskPremium', 'SMB1': 'SMB', 'HML1': 'HML'})
tmv = tmv.rename(columns={'RiskPremium2': 'RiskPremium', 'SMB2': 'SMB', 'HML2': 'HML'})
fmv.iloc[:, 1].fillna(fmv.iloc[:, 1].mean())
fmv.iloc[:, 2].fillna(fmv.iloc[:, 2].mean())
fmv.iloc[:, 3].fillna(fmv.iloc[:, 3].mean())
tmv.iloc[:, 1].fillna(tmv.iloc[:, 1].mean())
tmv.iloc[:, 2].fillna(tmv.iloc[:, 2].mean())
tmv.iloc[:, 3].fillna(tmv.iloc[:, 3].mean())


final = sm.OLS('',data = fmv)
