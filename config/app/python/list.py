import sqlite3
from .parse import class_dic
import gzip
import pickle
import pandas as pd
from django.shortcuts import render


def search_data():  # 최신 10개 문서 정보 GET 메소드
    # DB 연결
    conn = sqlite3.connect('./db.sqlite3', isolation_level=None)
    cursor = conn.cursor()

    # query문 작성 후 DB 데이터 GET
    cursor.execute("SELECT id, title, category, tags FROM APP_DOCUMENT ORDER BY id DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()

    for i, row in enumerate(rows):
        rows[i] = list(row)

    return rows


def progress_data():    # 프로그래스 바 카테고리 데이터 GET
    # DB 연결
    conn = sqlite3.connect('./db.sqlite3', isolation_level=None)
    cursor = conn.cursor()

    # query문 작성 후 DB 데이터 GET
    cursor.execute('SELECT category FROM APP_DOCUMENT')
    rows = cursor.fetchall()
    conn.close()

    # 분류 카테고리 이외의 사용자 정의 카테고리 개수 처리
    category_amount = {}
    for i, row in enumerate(rows):
        if row[0] not in list(class_dic.values()):
            if '기타' not in list(category_amount.keys()):
                category_amount['기타'] = 1
            else:
                category_amount['기타'] += 1
        rows[i] = row[0]

    # 분류 카테고리 전체 개수 처리
    for category_value in class_dic.values():
        if rows.count(category_value) != 0:
            category_amount[category_value] = rows.count(category_value)

    # 프로그래스 바의 카테고리 개수 데이터 처리
    progressbar_data = []
    total_amount = len(rows)
    for category, amount in category_amount.items():
        percent = (amount / total_amount) * 100
        data = (category, percent)
        progressbar_data.append(data)

    # 데이터 정렬
    progressbar_data.sort(key=lambda x: -x[1])
    progressbar_key = []
    progressbar_value = []
    for data in progressbar_data:
        progressbar_key.append(data[0])
        progressbar_value.append(data[1])

    return progressbar_key, progressbar_value


def issue_tag(db_len):  # 이슈 태그의 tags 데이터 GET
    if db_len != 0:
        with gzip.open('./app/dataset/tag_series.pickle', 'rb') as f:
            saved_tag = pickle.load(f)

        top_tag = saved_tag.head(10)
        tag_list = []
        for tag_name, tag_amount in top_tag.items():
            data = [tag_name, tag_amount]
            tag_list.append(data)
        return tag_list


def post_doc(request):  # list.py 파일 미들웨어 메소드
    # 최신 10개 문서 정보 GET
    title_list = search_data()
    list_len = int(len(title_list))
    context = {'post_len': list_len, 'post_list': title_list}

    # 프로그래스 바 데이터 GET
    key, value = progress_data()
    category_len = int(len(key))
    context['progressbar_key'] = key
    context['progressbar_value'] = value
    context['progressbar_len'] = category_len

    # 이슈 태그 데이터 GET
    tag_list = issue_tag(list_len)
    context['tag_list'] = tag_list

    return render(request, './app/document_list.html', context)