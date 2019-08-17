# -*- coding: utf-8 -*-
import jieba.analyse
import jieba.posseg
import xlrd


def get_line_from_path(excel_path, start_row, selected_col):  # 根据路径读取Excel文件，并从中按行提取数据

    data = xlrd.open_workbook(excel_path)
    table = data.sheets()[0]
    nrows = table.nrows

    list = []

    for i in range(start_row, nrows):
        line = ""
        row_values = table.row_values(i)
        for word in row_values[selected_col]:
            if word == "\n":
                list.append(line)
                line = ""
                continue
            line += word
        list.append(line)
    return list


def get_line_from_data(data, start_row, selected_col):  # 直接读取Excel文件，并从中按行提取数据
    table = data.sheets()[0]
    nrows = table.nrows

    row_list = []
    for i in range(start_row, nrows):
        line_list = []
        line = ""
        row_values = table.row_values(i)
        for word in row_values[selected_col]:
            if word == "\n":
                line_list.append(line)
                line = ""
                continue
            line += word
        line_list.append(line)
        row_list.append(line_list)
    return row_list


def remove_useless(sentence):  # 去除空格与数字
    sentence = sentence.replace(" ", "")

    for word in sentence:
        if word.isdigit():
            sentence = sentence.replace(word, "")

    return sentence


def seg2words_long(sentence):  # 切分并保留大于等于2长度的词
    seg_list = jieba.cut(sentence, HMM=True)
    word_list = []
    for word in seg_list:
        if len(word) > 1:
            word_list.append(word)

    return word_list


def seg2words_all(sentence):  # 切分并保留所有词
    seg_list = list(jieba.cut(sentence, HMM=True))
    return seg_list


def seg2keywords(sentence):  # 切分并保留关键词
    kWords = jieba.analyse.extract_tags(sentence, topK=10)
    return kWords


def tag(sentence):  # 词性标注
    words = jieba.posseg.cut(sentence)
    return words


def get_num_words(train_data_path, test_data_path):  # 分别读取两个文件中单句话的最大词数，取出最高者
    f1 = open(train_data_path)
    f1.readline()  # 跳过该行
    num_words1 = int(f1.readline())
    f2 = open(test_data_path)
    f2.readline()  # 跳过该行
    num_words2 = int(f2.readline())
    if num_words1 >= num_words2:
        return num_words1
    else:
        return num_words2
