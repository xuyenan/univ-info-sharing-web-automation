from webAuto import *
import pandas as pd
import time
import os


# 根据分数查找排名
def score2ranke(score: int, year: int, subject: str):

    path = './res/rankedList/'
    exts = 'li.csv' if subject == '理科' else 'wen.csv'    
    fileName = path + str(year) + exts

    df = pd.read_csv(fileName)
    maxScore = df.loc[0][0]
    if score > maxScore:
        return -1  # 前几十名查不到名次
    if score < 500:
        return 99999 # 未录入500分以下的名次
    return df.loc[maxScore - score][1]
 

def process():

    path = './res/data/'
    files = os.listdir(path)
    oringals = [f for f in files if f[:2] == '志愿']
    finals = [f for f in files if f not in oringals]
    preProcess = max(oringals) # 最新的导出数据
    oldProcess = max(finals)   # 上次的处理数据

    pre = pd.read_csv(path + preProcess, encoding='GB2312')
    old = pd.read_csv(path + oldProcess, encoding='utf8')

    oldLastIndex = old.iloc[-1].to_list()[1]   # 上次处理数据的最后一个答题序号
    pre = pre.loc[pre['答题序号'] > oldLastIndex]

    # 计算加分后的名次
    pre['addedScore'] = pre['Q4_高考分数'] + pre['Q5_少数民族加分']
    addedScore = list(pre['addedScore'])
    yer = list(pre['Q2_录取年份'])
    sub = list(pre['Q3_高中分科'])
    rankeList = list(map(lambda x, y, z: score2ranke(x, y, z), addedScore, yer, sub))
    pre['rankeList'] = rankeList

    csvFile = path + time.strftime('%y%m%d%H%M%S', time.localtime()) + '.csv'
    pre.to_csv(csvFile)

    return csvFile


# 填写表格
def fillTable(csvFile):

    # 登录
    wd = webInit()
    login(wd)
    sleep(5)

    df = pd.read_csv(csvFile, encoding='utf8')
    for row in df.itertuples():
        addRow(wd, list(row[1:]))

    print('----------------------done!-----------------------------')
    sleep(10)


if __name__ == '__main__':
    f = process()
    fillTable(f)


