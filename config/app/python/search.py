from .parse import preprocessing
from rank_bm25 import BM25Okapi
import gzip
import pickle
import sqlite3
from .parse import class_dic
from django.shortcuts import render


id_data = []


def get_search_data(search_index):
    conn = sqlite3.connect('./db.sqlite3', isolation_level=None)
    cursor = conn.cursor()

    search_data = []
    for index_id in search_index:
        cursor.execute(f"SELECT id, title, category, tags FROM APP_DOCUMENT WHERE id = {index_id}")
        search_data.append(list(cursor.fetchall()[0]))
    conn.close()
    return search_data


def progress_data(search_data):
    category_data = []
    for data in search_data:
        category_data.append(data[2])

    category_amount = {}
    for i, category in enumerate(category_data):
        if category not in list(class_dic.values()):
            if '기타' not in list(category_amount.keys()):
                category_amount['기타'] = 1
            else:
                category_amount['기타'] += 1

    for category in list(class_dic.values()):
        if category_data.count(category) != 0:
            category_amount[category] = category_data.count(category)

    total_len = len(search_data)
    category_list = [(key, value/total_len * 100) for key, value in category_amount.items()]
    category_list.sort(key=lambda x: -x[1])

    progress_key = [data[0] for data in category_list]
    progress_value = [data[1] for data in category_list]

    return progress_key, progress_value


def search_processing(request):
    query = request.GET.get('keyword')
    token_query = preprocessing(query)

    with gzip.open('./app/dataset/corpus_for_search.pickle', 'rb') as f:
        token_corpus = pickle.load(f)

    search_model = BM25Okapi(token_corpus)

    score = list(search_model.get_scores(token_query))
    search_index = []
    for i in range(20):
        if max(score) == 0.0:
            break
        elif max(score) < 0.0:
            break
        else:
            index = score.index(max(score))
            search_index.append(index)
            score[index] = 0.0

    search_data = get_search_data(search_index)

    context = {}
    # category_search.py 에서 사용 하는 데이터
    for data in search_data:
        id_data.append(data[0])
    context['id_data'] = id_data

    result_len = int(len(search_data)) + 1
    context['query'] = query
    context['post_len'] = result_len
    context['post_list'] = search_data

    key, value = progress_data(search_data)
    progress_len = len(key)

    context['progressbar_key'] = key
    context['progressbar_value'] = value
    context['progressbar_len'] = progress_len

    return render(request, './app/document_search.html', context)