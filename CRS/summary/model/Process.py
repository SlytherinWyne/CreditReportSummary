# -*- coding: utf-8 -*-
import random
import numpy as np
import Word2Vec as wv
import Util as u

train_excel_path = "./data/process/train.xlsx"
test_excel_path = "./data/process/test.xlsx"
train_data_path = "./data/process/train_data.txt"
test_data_path = "./data/process/test_data.txt"

size = 100


def save_train_data():  # 从Excel文件中提取训练数据，存储至txt文件
    line_list = u.get_line_from_path(train_excel_path, 4, 2)
    save_data(line_list, train_data_path, False)


def save_test_data():  # 从Excel文件中提取测试数据，存储至txt文件
    line_list = u.get_line_from_path(test_excel_path, 4, 2)
    save_data(line_list, test_data_path, False)


def load_all_data(train_data_path, test_data_path):  # 读取所有数据
    num_words = u.get_num_words(train_data_path, test_data_path)

    x_train, y_train = load_data(train_data_path, num_words)
    x_test, y_test = load_data(test_data_path, num_words)

    return x_train, y_train, x_test, y_test


def save_data(line_list, data_path, ignore):

    num_lines = 0
    largest_num = 0

    vector_model = wv.load_model()

    for i in range(len(line_list)):
        if (i+1) % 50 == 0:
            print("第" + str(i+1) + "行 (" +  str(i+1) + "/" + str(len(line_list)) + ")")

        # 清除无关信息
        line_list[i] = u.remove_useless(line_list[i])

        # 处理标签
        label = 0
        if "|" in line_list[i]:
            label = 1
            line_list[i] = line_list[i].replace("|", "")
        else:
            if ignore:
                if random.randint(0,9) < 3:
                    label = 0
                else:
                    continue
            else:
                label = 0

        # 转换为词向量
        total_vector = []
        word_list = u.seg2words_long(line_list[i])
        for word in word_list:
            word = word.encode('utf-8')
            vector = wv.get_vector(vector_model, word) # 模型是utf-8的
            if(vector == []):
                continue
            total_vector.append(vector)

        # 找到最大值
        if len(total_vector) > largest_num:
            largest_num = len(total_vector)

        # 去除空行
        if total_vector == []:
            continue

        num_lines += 1

        # 写入数据
        f = open(data_path, "a")
        f.write(str(label) + "\n")
        for vector in total_vector:
            for num in vector:
                f.write(str(num) + " ")
            f.write("\n")
        f.write("%\n")
        f.close()

    # 在开头两行补上数据的维度，以供在训练的初始化时提取
    f = open(data_path, 'r+')
    content = f.read()
    f.seek(0, 0)
    f.write(str(num_lines) + "\n")
    f.write(str(largest_num) + "\n")
    f.write(content)
    f.close()


def load_data(data_path, num_words):
    f = open(data_path)
    num_lines = int(f.readline())
    f.readline()  # 跳过

    data = np.empty((num_lines, num_words, size), dtype="float64")
    label = np.empty(num_lines, dtype="float64")

    for i in range(num_lines):
        line = f.readline()  #
        label[i] = np.float64(line)
        line = f.readline()#读取一个词
        num = 0
        while line != "%":
            nums = line.split(" ")
            vector = np.empty(size, dtype="float64")
            for j in range(size):
                vector[j] = np.float64(nums[j])
            data[i, num, :] = vector
            num += 1
            line = f.readline()
            line = line.replace("\n", "")  # 去掉换行符

        for j in range(num, num_words):
            data[i, j, :] = -1
    f.close()
    return data, label

#save_train_data() # 从Excel文件中提取训练数据，存储至txt文件
#save_test_data() # 从Excel文件中提取测试数据，存储至txt文件