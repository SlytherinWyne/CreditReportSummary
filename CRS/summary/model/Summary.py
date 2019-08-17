# -*- coding: utf-8 -*-
from pyltp import SentenceSplitter
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import Parser
import os

import Util as u

abs_dir = __file__[:__file__.rfind("/")]
LTP_DATA_DIR = abs_dir + '/data/ltp_data'
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')


class Word():
    def __init__(self, index, text, tag, head, relation):
        self.index = index
        self.text = text
        self.tag = tag
        self.head = head
        self.relation = relation

    def show(self):
        print (self.text)
        print(self.index, self.text, self.tag, self.head, self.relation)


def seg2sentences(text):  # 拆分成句子
    sents = SentenceSplitter.split(text)
    return sents


def seg2words(sentence):  # 拆分成单词（已用jieba替代）
    segmentor = Segmentor()
    segmentor.load(cws_model_path)
    words = segmentor.segment(sentence)
    segmentor.release()  # 释放模型
    return words


def tag(words):  # 词性标注
    postagger = Postagger()
    postagger.load(pos_model_path)
    postags = postagger.postag(words)
    postagger.release()  # 释放模型
    return postags


def keep_core(sentence):
    # 保留冒号后的
    if sentence.find("：") != -1:
        sentence = sentence.split("：")[1]

    # 去除关联词中不重要的部分
    remove_list = ["因", "因为", "如果", "如", "鉴于", "由于"]
    for word in remove_list:
        if sentence.find(word) >= 0:
            sentence = sentence.split(word, 1)[1].split("，", 1)[1]
            break

    return sentence

def parse(text):  # 句法依存标注

    sentences = seg2sentences(text)
    parser = Parser()
    parser.load(par_model_path)
    arcs_list = []

    for sentence in sentences:
        sentence = keep_core(sentence)
        word_list = u.seg2words_all(sentence)
        words = []
        for word in word_list:
            words.append(word.encode('utf-8'))
        postags = tag(words)

        # 两种词性标注都有各自好用的时候
        '''
        tag_list = u.tag(sentence)
        words = []
        postags = []
        for word, tag in tag_list:
            words.append(word.encode('utf-8'))
            postags.append(tag.encode('utf-8'))
        '''

        arcs = parser.parse(words, postags)
        list = []
        for i in range(len(words)):
            word = Word(i+1, words[i], postags[i], arcs[i].head, arcs[i].relation)
            word.show()
            list.append(word)
        arcs_list.append(list)
    parser.release()  # 释放模型
    return arcs_list


def find_relative(words_list, word):  # 找到相关词
    relative_list = []
    for w in words_list:
        if w.head == word.index:
            relative_list.append(w)
    return relative_list


def find_all_relative(words_list, word):  # 通过递归找到所有相关词
    all_relative_list = []
    relative_list = find_relative(words_list, word)
    if relative_list != []:
        for r_outer in relative_list:
            # 拆分HED为动词情况下的并列结构
            if (word.relation == "HED" or word.relation == "VOB" or word.relation == "COO") and r_outer.relation == "COO":
                continue
            all_relative_list.append(r_outer)
            list = find_all_relative(words_list, r_outer)
            if list != []:
                for r_inner in list:
                    all_relative_list.append(r_inner)
    return all_relative_list


def relative_sentence(words_list, word):  # 得到以当前动词为主的句子

    relative_list = find_all_relative(words_list, word)
    line = ""

    if relative_list != []:
        for i in range(len(relative_list)):
            for j in range(i, len(relative_list)):
                if relative_list[i].index > relative_list[j].index:
                    relative_list[i], relative_list[j] = relative_list[j], relative_list[i]

        while relative_list[-1].relation == "WP":
            relative_list.remove(relative_list[-1])

        for w in relative_list:
            if w.index > word.index:
                line += w.text

    adv = ""
    for adv_word in words_list:
        if adv_word.head == word.index and adv_word.index == word.index - 1 and adv_word.relation == "ADV":
            adv = adv_word.text
            break
    return adv, line


def get_summary(text):  # 摘要
    sents_list = parse(text)
    summary_list = []
    for sent in sents_list:
        for word in sent:
            if word.head == 0:
                coo_list = [word.index]
                if word.tag == "v":
                    adv, sentence = relative_sentence(sent, word)
                    if sentence != "":
                        summary_list.append([adv + word.text, sentence])

                for relative_word in sent:
                    if relative_word.head == word.index and relative_word.relation == "VOB":
                        coo_list.append(relative_word.index)
                        if word.tag != "v" and relative_word.tag == "v":
                            adv, sentence = relative_sentence(sent, relative_word)
                            if sentence != "":
                                summary_list.append([adv + relative_word[1], sentence])

                        '''
                        if summary_list != []:
                            for i_summary in range(len(summary_list)):
                                if summary_list[i_summary][0].index > word.index:
                                    summary_list.insert(i_summary, [adv + word.text, sentence])
                                    break
                        else:
                        '''

                for coo_word in sent:
                    if coo_word.tag == "v" and coo_word.head in coo_list and coo_word.relation == "COO":
                        coo_list.append(coo_word.index)
                        adv, sentence = relative_sentence(sent, coo_word)
                        if sentence != "":
                            summary_list.append([adv + coo_word.text, sentence])
                break
    return summary_list

def test():
    text = "要求信管部和个贷部发函明确落实豪门府邸按揭款专项用于该户还款，优先收回风险大的授信主体贷款；"

    for summary in get_summary(text):
        print(summary[0] + " " + summary[1])

test()
