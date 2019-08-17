# -*- coding: utf-8 -*-
import keras
from keras.models import load_model
import numpy as np

import Word2Vec as wv
import Util as u

abs_dir = __file__[:__file__.rfind("/")]
train_data_path = abs_dir + "/data/process/train_data.txt"
test_data_path = abs_dir + "/data/process/test_data.txt"
model_path = abs_dir + "/data/train/model.h5"

size = 100


def predict(sentence, num_words, model):  # 预测此句是否为要点句，是返回1，不是返回0
    data = np.empty((1, num_words, size), dtype="float64")

    sentence = u.remove_useless(sentence)
    word_list = u.seg2words_long(sentence)
    word_list = word_list[:num_words]  # 把长度缩减到训练模型的长度
    num = 0

    vector_model = wv.load_model()
    for i in range(len(word_list)):
        word = word_list[i].encode('utf-8')
        vector = wv.get_vector(vector_model, word)
        if vector == []:
            continue

        data[0, i, :] = vector
        num += 1

    for j in range(num, num_words):
        data[0, j, :] = -1

    prediction = model.predict(data)
    # print "%.2f%%" % (float(prediction[0][0]) * 100) + " " + "%.2f%%" % (float(prediction[0][1]) * 100)
    return np.argmax(prediction)


def get_focus(data):  # 从Excel中获取要点句
    data_list = u.get_line_from_data(data, 2, 2)   ##
    num_words = u.get_num_words(train_data_path, test_data_path)
    model = load_model(model_path)

    summary_list = []

    for i in range(len(data_list)):
        line_list = []
        for j in range(len(data_list[i])):
            prediction = predict(data_list[i][j], num_words-1, model)  ##
            if prediction == 1:
                line_list.append(data_list[i][j])
                print (data_list[i][j].encode('utf-8'))  ##
                print ('\n')
        summary_list.append(line_list)
    keras.backend.clear_session()

    return summary_list

import xlrd
excel_path = "./data/process/test.xlsx"
data = xlrd.open_workbook(excel_path)
get_focus(data)