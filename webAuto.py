# 自动填写表格 https://www.wolai.com/k7pkLRRhb44Z7XHc5f9MaQ
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep
import json
import re


def webInit():
    options = webdriver.ChromeOptions()
    options.add_argument('-ignore-certificate-errors')
    options.add_argument('-ignore -ssl-errors')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    wd = webdriver.Chrome(options=options)
    url = 'https://www.wolai.com/login'

    wd.get(url)
    wd.implicitly_wait(20)
    return wd


def login(wd: webdriver):
    with open('./res/login.txt', 'r', encoding='utf8') as f:
        loginTxt = json.loads(f.read())
    id = loginTxt['phone']
    pw = loginTxt['password']

    inputID = wd.find_element(By.CSS_SELECTOR, '.form-control')
    inputID.send_keys(id + '\n')
    inputPw = wd.find_element(By.CSS_SELECTOR, '._3VFoh > input')
    inputPw.send_keys(pw + '\n')


# 增加一条信息
def addRow(wd: webdriver, dataList: list):
    
    # 新增一空行
    addNew = wd.find_element(By.CSS_SELECTOR, '._2OmeE._3sMqb.node-btn')
    addNew.click()
    wd.switch_to.active_element.send_keys(Keys.ALT, 'q')


    # 表格 2:大学 3:入学时间 4:分科 5:国家专项 6:排名 7:专业 8:认识 9:联系方式
    # 数据列表 3:大学 4:入学时间 5:分科 8:国家专项 -1:排名 9:专业 10:专业认识 11:联系
    dataList = list(map(str, dataList))
    
    # 大学名称
    anchor = f'[data-index="0"]>div>div>div:nth-child(2)'
    wd.find_element(By.CSS_SELECTOR, anchor).click()
    wd.switch_to.active_element.send_keys(getUni(dataList[3]) +'\n')

    # 入学时间
    anchor = f'[data-index="0"]>div>div>div:nth-child(3)'
    wd.find_element(By.CSS_SELECTOR, anchor).click()
    wd.switch_to.active_element.send_keys(dataList[4] + '\n')

    # 分科
    anchor = f'[data-index="0"]>div>div>div:nth-child(4)'
    wd.find_element(By.CSS_SELECTOR, anchor).click()
    if dataList[5] == '理科':
        wd.find_element(By.CSS_SELECTOR, '#tag-list>div>div').click()
    else:
        wd.find_element(By.CSS_SELECTOR,'#tag-list>div>div:nth-child(2)').click()

    # 国家专项
    if dataList[8] == '是':
        anchor = f'[data-index="0"]>div>div>div:nth-child(5)'
        wd.find_element(By.CSS_SELECTOR, anchor).click()

    # 省排名
    anchor = f'[data-index="0"]>div>div>div:nth-child(6)'
    wd.find_element(By.CSS_SELECTOR, anchor).click()
    wd.switch_to.active_element.send_keys(dataList[-1] + '\n')
    # 专业
    anchor = f'[data-index="0"]>div>div>div:nth-child(7)'
    wd.find_element(By.CSS_SELECTOR, anchor).click() 
    fillGrid(wd.switch_to.active_element, dataList[9])
    
    # 联系方式
    anchor = f'[data-index="0"]>div>div>div:nth-child(9)'
    wd.find_element(By.CSS_SELECTOR, anchor).click()
    fillGrid(wd.switch_to.active_element, dataList[11])
    
    # 专业认识  这部分内容较多，可能会引起网页出故障，所以放在最后，并留足时间
    anchor = f'[data-index="0"]>div>div>div:nth-child(8)'
    wd.find_element(By.CSS_SELECTOR, anchor).click()
    fillGrid(wd.switch_to.active_element, dataList[10])
    sleep(8)
    

# 提取大学名称，提取前：xx省 | xx市 | xx大学
def getUni(s):
    pattern = re.compile('.*?\|.*?\|\s*(.*)')
    return pattern.match(s).group(1)


# 处理含'\n''\t'的信息的填写
def fillGrid(wd_element, sentence: str):
    for s in sentence.split(sep='\n'):
        s = s.replace('\t', 'tab')
        wd_element.send_keys(s)
        wd_element.send_keys(Keys.SHIFT, '\n')
        sleep(1)
    wd_element.send_keys(Keys.BACKSPACE)
    wd_element.send_keys('\n')



# 仅用于测试该模块
if __name__ == '__main__':

    wd = webInit()
    login(wd)
    sleep(5)

    dataListEm = ['0', '1', '', '北京市 | 北京市 | 清华大学', '2021', '理科', '671', '10', '是', '机航动大类车辆学院电子信息方向',
     'test1\ntest2\ttest3   test4', '邮箱 guil21@qq.com', '2023-01-24 23: 00: 58', '2023-01-24 23: 04: 17', '3分19秒', '四川省', '达州市', '117.139.69.136', 'ChromiumEdge 109.0.1518.61', 'Windows 10',
      '681', '469']
    addRow(wd, dataListEm)
