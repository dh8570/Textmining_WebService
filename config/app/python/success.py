import sqlite3
import pandas as pd
from .list import post_doc
from .parse import preprocessing
import pickle
import gzip


def insert_data(insert_set):
    # connecting DB
    conn = sqlite3.connect('./db.sqlite3', isolation_level=None)
    # connecting cursor
    cursor = conn.cursor()

    cursor.execute("INSERT INTO APP_DOCUMENT(id, category, document, title, tags) VALUES(?, ?, ?, ?, ?)", insert_set)
    conn.close()


def get_data_amount():
    conn = sqlite3.connect('./db.sqlite3', isolation_level=None)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM APP_DOCUMENT")
    rows = cursor.fetchall()
    index = len(rows)

    return index


# 검색을 위한 문서 코퍼스 저장
def search_model(doc, db_amount):
    token_corpus = preprocessing(doc)

    # DB에 값이 없을 때 수행
    if db_amount == 0:
        with gzip.open('./app/dataset/corpus_for_search.pickle', 'wb') as f:
            pickle.dump([token_corpus], f)
    else:
        with gzip.open('./app/dataset/corpus_for_search.pickle', 'rb') as f:
            saved_corpus = pickle.load(f)

        saved_corpus.append(token_corpus)
        with gzip.open('./app/dataset/corpus_for_search.pickle', 'wb') as f:
            pickle.dump(saved_corpus, f)


def tagging(text):
    word_list = pd.Series(text)
    freq_words = word_list.value_counts()
    return freq_words


def save_tag(doc, db_amount):
    text = preprocessing(doc)
    tag_series = tagging(text)

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


def get(request):
    title = request.GET.get('title')
    doc = request.GET.get('document')
    category = request.GET.get('category')
    tags = request.GET.get('tags')

    if (title is None) and (doc is None) and (category is None) and (tags is None):
        return post_doc(None)
    else:
        db_amount = get_data_amount()
        search_model(doc, db_amount)
        save_tag(doc, db_amount)
        insert_set = [db_amount, category, doc, title, tags]

        insert_data(insert_set)

        return post_doc(None)