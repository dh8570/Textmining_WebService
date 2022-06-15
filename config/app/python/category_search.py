from .search import id_data
import sqlite3
from django.shortcuts import render


def category_search_processing(request):    # 검색 후 특정 카테고리의 검색 결과만 확인 하기 위한 메소드
    # request 데이터 GET
    category = request.GET.get('category')
    connect_id = list(dict.fromkeys(id_data))

    # DB 연결
    conn = sqlite3.connect('./db.sqlite3')
    cursor = conn.cursor()

    # query문 작성 후 DB 데이터 GET
    search_data = []
    for id_value in connect_id:
        cursor.execute(f"SELECT id, title, category, tags FROM APP_DOCUMENT WHERE id = {id_value} AND category='{category}'")
        rows = cursor.fetchone()
        if rows is not None:
            search_data.append(list(rows))
    conn.close()

    rows_len = int(len(search_data))

    # 전송 context 생성
    context = {
        'post_amount': rows_len,
        'post_list': search_data
    }

    return render(request, './app/search_by_category.html', context)