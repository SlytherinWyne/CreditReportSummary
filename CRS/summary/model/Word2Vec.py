# -*- coding: utf-8 -*-
from gensim.models import word2vec
import Util as u

abs_dir = __file__[:__file__.rfind("/")]
excel_path = abs_dir + "/data/word2vec/dataset1.xlsx"
corpus_path = abs_dir + "/data/word2vec/corpus.txt"
model_path = abs_dir + "/data/word2vec/vector"


def get_corpus():
    line_list = u.get_line_from_path(excel_path, 5, 2)

    f = open(corpus_path, "a")

    for line in line_list:
        line = u.remove_useless(line)
        word_list = u.seg2words_long(line)

        if len(word_list) == 0:
            continue

        for word in word_list:
            word = word.encode('utf-8')
            f.write(word + " ")
        f.write("\n")

    f.close()


def learn():  # 生成的模型是utf-8的
    f = open(corpus_path)
    line = f.readline()
    sentences = []
    while line:
        sentence = line.split(" ")
        sentences.append(sentence)
        line = f.readline()
    f.close()
    model = word2vec.Word2Vec(sentences)#size=100
    model.save(model_path)


def load_model():
    model = word2vec.Word2Vec.load(model_path)
    return model


def get_vector(model, word):  # 计算词的词向量
    try:
        vector = model[word]
    except:
        return []
    return vector


def get_similarity(word1, word2):  # 通过计算词向量，得到两词之间的相似度
    model = word2vec.Word2Vec.load(model_path)
    return model.similarity(word1, word2)

#get_corpus()  # 从Excel文件中筛选词语，生成语料
#learn()  # 根据语料进行学习，生成词向量模型
