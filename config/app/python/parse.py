from eunjeon import Mecab
import re
from django.shortcuts import render
import pandas as pd
from ..apps import classificator


class_dic = {   # 분류 카테고리
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


def preprocessing(text):    # 태깅 작업을 위한 문서 불용어 제거 및 토크나이징
    # 불용어 제거
    text = re.sub('\W', ' ', str(text))
    text = re.sub('\n|\t', ' ', text)
    text = re.sub('\s+', ' ', text)
    text = text.strip()

    # Mecab 토그나이징
    mecab = Mecab()
    pos = ['NNG', 'NNP', 'NP', 'SL']
    text = [morph for morph, tag in mecab.pos(text) if tag in pos]

    return text


def preprocessing_classification(text):     # 카테고리 분류를 위한 문서 불용어 제거
    # 불용어 제거
    text = re.sub('\W', ' ', str(text))
    text = re.sub('\n|\t', ' ', text)
    text = re.sub('\s+', ' ', text)
    text = text.strip()

    return text


def tagging(prep_list):     # 태그 리스트 정렬 및 상위 태그 GET
    # 태그 리스트 처리 용이성을 위해 Series 형태로 변환
    word_list = pd.Series(prep_list)
    # 단어 개수 추출 후 상위 단어 추출
    freq_words = word_list.value_counts().head(5)
    return freq_words


def get_label(result):  # BERT 분류 모델 결과 label 후처리
    result = result[0]['label']

    # 분류 모델 결과 값에서 정수형 데이터 추출 작업
    if int(len(result)) == 8:
        result = int(result[-2:])
    else:
        result = int(result[-1])

    # 정수형 레이블 -> 문자형 카테고리로 변환
    result_label = class_dic[result]

    return result_label


def get_and_processing(request):    # parse.py 미들웨어 메소드
    # request 정보 GET
    title = request.GET.get('title')
    doc = request.GET.get('document')

    # 불용어 제거
    preprocessed_data = preprocessing(doc)

    # 태그 작업을 위한 태깅
    freq_words = tagging(preprocessed_data)
    freq_text = ""
    for key in freq_words.keys():
        freq_text = freq_text + '#' + key + ' '
    freq_text = freq_text.strip()

    # 문서 분류 작업
    result = classificator[0](preprocessing_classification(doc))
    result_label = get_label(result)

    # 백엔드 처리 데이터 Set 생성 및 전달
    context = {'title': title, 'document': doc, 'category': result_label, 'tags': freq_text}
    print(request.path)
    return render(request, './app/document_create.html', context)