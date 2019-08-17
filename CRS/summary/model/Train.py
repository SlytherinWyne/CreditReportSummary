# -*- coding: utf-8 -*-
import datetime
import time

from keras.callbacks import TensorBoard
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM, Masking, Bidirectional
import numpy as np
import Process as p

model_path = "./data/train/model.h5"

batch_size = 32
epochs = 50

# 辅助方法


def categorical(label):  # 使标签变成one—hot形式
    length = label.shape[0]
    c = np.zeros((length, 2))
    for i in range(length):
        c[i,int(label[i])] = 1
    return c


def check_balance(label):  # 检查数据是否平衡
    total = 0
    zero = 0
    for i in label:
        total += 1
        if i == 0:
            zero += 1

    print(str(float(zero) / float(total)))


def convert_time(time):  # 将秒转换为时分秒
    hours = int(time/3600)
    minutes = int((time % 3600)/60)
    seconds = int(time % 60)
    return str(hours) + "h " + str(minutes) + "m " + str(seconds) + "s"

# 模型与训练


def lstm_model():  # 模型
    model = Sequential()
    model.add(Masking(mask_value=-1, input_shape=input_shape))
    model.add(Bidirectional(LSTM(64, return_sequences=True)))
    model.add(Dropout(0.2))
    model.add(Bidirectional(LSTM(64, return_sequences=True)))
    model.add(Dropout(0.2))
    model.add(Bidirectional(LSTM(128)))
    model.add(Dropout(0.2))
    model.add(Dense(2, activation='softmax'))
    return model


x_train, y_train, x_test, y_test = p.load_all_data(p.train_data_path, p.test_data_path)
y_train = categorical(y_train)
y_test = categorical(y_test)
input_shape = (x_train.shape[1], x_train.shape[2])

model = lstm_model()
model.compile(optimizer="rmsprop", loss="categorical_crossentropy", metrics=["accuracy"])

start_train = time.time()
tensorboard = TensorBoard(log_dir="data/train/logs/{:%Y%m%d%H%M}".format(datetime.datetime.now()))
#tensorboard --logdir PycharmProjects/CreditReportSummary/summary/model/data/train/logs/
#http://localhost:6006/

model.fit(x_train,
          y_train,
          batch_size=batch_size,
          epochs=epochs,
          validation_data=(x_test, y_test),
          callbacks=[tensorboard])

time_train = convert_time(time.time() - start_train)  # Time for training.
print("训练耗时" + time_train)

model.save(model_path)  # 保存模型
print("Model saved!")
