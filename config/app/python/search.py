from .parse import preprocessing
from rank_bm25 import BM25Okapi
import gzip
import pickle
import sqlite3
from django.shortcuts import render


def get_search_data(search_index):
    conn = sqlite3.connect('./db.sqlite3', isolation_level=None)
    cursor = conn.cursor()

    search_data = []
    for index_id in search_index:
        cursor.execute(f"SELECT id, title, category, tags FROM APP_DOCUMENT WHERE id = {index_id}")
        search_data.append(list(cursor.fetchall()[0]))
    conn.close()
    return search_data


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
        else:
            index = score.index(max(score))
            search_index.append(index)
            score[index] = 0.0

    search_data = get_search_data(search_index)

    context = {}
    result_len = int(len(search_data)) + 1
    for i in range(result_len):
        if i == 0:
            context['query'] = query
        else:
            context[f'result{i}'] = search_data[i-1]

    return render(request, './app/document_search.html', context)
