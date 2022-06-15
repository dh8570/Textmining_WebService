import sqlite3
import pandas as pd
from .list import post_doc
from .parse import preprocessing
import pickle
import gzip


def insert_data(insert_set):    # 문서 정보 DB에 저장
    # DB 연결
    conn = sqlite3.connect('./db.sqlite3', isolation_level=None)
    cursor = conn.cursor()

    # query문 작성 후 DB에 데이터 저장
    cursor.execute("INSERT INTO APP_DOCUMENT(id, category, document, title, tags) VALUES(?, ?, ?, ?, ?)", insert_set)
    conn.close()


def get_data_amount():  # 전체 데이터 개수 GET 메소드
    # DB 연결
    conn = sqlite3.connect('./db.sqlite3', isolation_level=None)
    cursor = conn.cursor()

    # query문 작성 후 DB 데이터 GET
    cursor.execute("SELECT * FROM APP_DOCUMENT")
    rows = cursor.fetchall()
    index = len(rows)

    return index


def search_model(doc, db_amount):   # 검색을 위한 코퍼스 저장 메소드
    # 문서 데이터 불용어 제거
    token_corpus = preprocessing(doc)

    # 문서 코퍼스 저장
    if db_amount == 0:
        with gzip.open('./app/dataset/corpus_for_search.pickle', 'wb') as f:
            pickle.dump([token_corpus], f)
    else:
        with gzip.open('./app/dataset/corpus_for_search.pickle', 'rb') as f:
            saved_corpus = pickle.load(f)

        saved_corpus.append(token_corpus)
        with gzip.open('./app/dataset/corpus_for_search.pickle', 'wb') as f:
            pickle.dump(saved_corpus, f)


def tagging(text):  # 데이터 태깅 작업
    word_list = pd.Series(text)
    freq_words = word_list.value_counts()
    return freq_words


def save_tag(doc, db_amount):   # 태그 작업을 위한 태깅 데이터 저장
    # 문서 불용어 제거 및 태깅 작업
    text = preprocessing(doc)
    tag_series = tagging(text)

    # 태깅된 정보 저장
    if db_amount == 0:
        with gzip.open('./app/dataset/tag_series.pickle', 'wb') as f:
            pickle.dump(tag_series, f)
    else:
        with gzip.open('./app/dataset/tag_series.pickle', 'rb') as f:
            saved_tag = pickle.load(f)

        for tag_name, tag_amount in tag_series.items():
            if tag_name not in list(saved_tag.keys()):
                saved_tag[tag_name] = tag_amount
            else:
                saved_tag[tag_name] += tag_amount
        saved_tag = saved_tag.sort_values(ascending=False)
        print(saved_tag)
        with gzip.open('./app/dataset/tag_series.pickle', 'wb') as f:
            pickle.dump(saved_tag, f)


def get(request):   # success.py 미들웨어 메소드
    # request 데이터 GET
    title = request.GET.get('title')
    doc = request.GET.get('document')
    category = request.GET.get('category')
    tags = request.GET.get('tags')

    # 데이터 문제가 없을 시 수행
    if (title is None) and (doc is None) and (category is None) and (tags is None):
        return post_doc(None)
    else:
        # 사용자 입력 문서 데이터 DB에 저장
        db_amount = get_data_amount()
        search_model(doc, db_amount)
        save_tag(doc, db_amount)
        insert_set = [db_amount, category, doc, title, tags]

        insert_data(insert_set)

        return post_doc(None)