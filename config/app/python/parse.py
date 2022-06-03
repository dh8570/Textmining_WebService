from eunjeon import Mecab
import re
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import csv
from tensorflow.keras.models import load_model
from django.shortcuts import render
import pandas as pd
import os


class_dic = {
    0: '청와대',
    1: '국회/정당',
    2: '북한',
    3: '행정',
    4: '국방/외교',
    5: '금융',
    6: '증권',
    7: '산업/재계',
    8: '중기/벤처',
    9: '부동산',
    10: '글로벌경제',
    11: '생활경제',
    12: '사건사고',
    13: '교육',
    14: '노동',
    15: '언론',
    16: '환경',
    17: '인권/복지',
    18: '식품/의료',
    19: '지역',
    20: '인물',
    21: '건강정보',
    22: '자동차/시승기',
    23: '도로/교통',
    24: '여행/레저',
    25: '음식/맛집',
    26: '패션/뷰티',
    27: '공연/전시',
    28: '책',
    29: '종교',
    30: '날씨',
    31: '아시아/호주',
    32: '미국/중남미',
    33: '유럽',
    34: '중동/아프리카',
    35: '모바일',
    36: '인터넷/SNS',
    37: '통신/뉴미디어',
    38: 'IT 일반',
    39: '보안/해킹',
    40: '컴퓨터',
    41: '게임/리뷰'
}


def tokenizer(data):
    vocab_size = 61519
    max_len = 400

    tok = Tokenizer(vocab_size, oov_token="OOV")
    train_data = []

    with open('./app/dataset/train_data.csv', 'r', encoding="UTF-8") as f:
        reader = csv.reader(f)
        for i, line in enumerate(reader):
            train_data.append(line)

    tok.fit_on_texts(train_data)
    data = tok.texts_to_sequences(data)
    pre_data = pad_sequences(data, maxlen=max_len)

    return pre_data


def preprocessing(text):
    text = re.sub('[\W]', ' ', str(text))
    text = re.sub('[\n|\t]', ' ', text)
    text = text.strip()

    mecab = Mecab()
    pos = ['NNG', 'NNP', 'NNBC', 'NP', 'SL']
    text = [morph for morph, tag in mecab.pos(text) if tag in pos]

    return text


def tagging(prep_list):
    word_list = pd.Series(prep_list)
    freq_words = word_list.value_counts().head(5)
    return freq_words

def get_and_processing(request):
    title = request.GET.get('title')
    doc = request.GET.get('document')

    # removing useless words
    preprocessed_data = preprocessing(doc)

    # tagging for tag works
    freq_words = tagging(preprocessed_data)
    freq_text = ""
    for key in freq_words.keys():
        freq_text = freq_text + '#' + key + ' '
    freq_text = freq_text.strip()
    print(freq_text)

    # tokenizing for categorical
    pre_data = tokenizer([preprocessed_data])

    # updating model
    model = load_model('./app/model/model.h5')
    decoder = load_model('./app/model/decoder.h5')

    # predicting data
    y_predict = model.predict(pre_data)
    y_predict = decoder(y_predict)
    result = list(y_predict.numpy()[0])
    result_idx = result.index(max(result))

    print(class_dic[result_idx])
    context = {'title': title, 'document': doc, 'category': class_dic[result_idx], 'tags': freq_text}
    print(request.path)
    return render(request, './app/document_create.html', context)