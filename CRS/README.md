# CreditReportSummary
The project is written in Python 2.7.10. After running the server, it can receive excel file and return summary data as JSON.

# 在本地运行服务器
1. 从命令行进入项目目录
2. python manage.py runserver 0.0.0.0:8000

# 文件结构

##  /summary/model
1. /summary/model/Word2Vec
    * 功能：
        1. 从Excel文件中筛选词语，生成语料
        2. 根据预料进行学习，生成词向量模型
    * 需要数据：/summary/model/data

2. /summary/model/Process
    * 功能：
        1. 从Excel文件中提取训练数据，存储至txt文件
        2. 从Excel文件中提取测试数据，存储至txt文件
        3. 读取txt数据
    * 需要数据：/summary/model/Process

3. /summary/model/Train
    * 功能：
        1. 运用LSTM神经网络训练机器进行学习
        2. 生成显示训练过程的图表
        3. 保存训练好的模型
    * 需要数据：/summary/model/Trian

4. /summary/model/Focus
    * 功能：
        1. 加载训练模型
        2. 运用模型对句子进行预测
    * 需要数据：/summary/model/Train
        
5. /summary/model/Summary
    * 功能：
        1. 生成摘要
    * 需要数据：/summary/model/ltp_data

6. /summary/model/Util
    * 功能：
        1. 通用辅助方法
        2. 句子与词语处理

# 开发前准备

## pip
* 版本: 10.0.1
* 安装: 
    1. 从命令行进入安装目录
    2. curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    3. python get-pip.py

## xlrd
* 版本: 1.1.0
* 安装: pip install xlrd

## Tensorflow
* 版本: 1.8.0
* 安装: pip install tensorflow

## Keras
* 版本: 2.2.0
* 安装: pip install keras

## Numpy
* 版本: 1.14.5
* 安装: pip install numpy

## Gensim
* 版本: 3.4.0
* 安装: pip install gensim

## Jieba
* 版本: 0.39
* 安装: pip install jieba

## pyltp
* 版本: 0.2.1
* 安装: 
    * MacOS: MACOSX_DEPLOYMENT_TARGET=10.13 pip install pyltp
    * Linux: pip install pyltp
    * Windows: pip install pyltp
    * 模型: https://pan.baidu.com/share/link?shareid=1988562907&uk=2738088569#list/path=%2F&parentPath=%2F

## Django
* 版本: 1.11.13
* 安装: pip install django==1.11.13

## django-cors-headers
* 版本: 2.2.0
* 安装: pip install django-cors-headers
