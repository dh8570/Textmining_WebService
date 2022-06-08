from .search import id_data
import sqlite3
from django.shortcuts import render


def category_search_processing(request):
    category = request.GET.get('category')
    connect_id = list(dict.fromkeys(id_data))

    conn = sqlite3.connect('./db.sqlite3')
    cursor = conn.cursor()

    search_data = []
    for id_value in connect_id:
        cursor.execute(f"SELECT id, title, category, tags FROM APP_DOCUMENT WHERE id = {id_value} AND category='{category}'")
        rows = cursor.fetchone()
        if rows is not None:
            search_data.append(list(rows))
    conn.close()

    rows_len = int(len(search_data))

    context = {
        'post_amount': rows_len,
        'post_list': search_data
    }

    print(context)
    return render(request, './app/search_by_category.html', context)