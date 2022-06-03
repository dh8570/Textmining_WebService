import sqlite3
from django.shortcuts import render


def search_data():
    conn = sqlite3.connect('./db.sqlite3', isolation_level=None)
    cursor = conn.cursor()

    cursor.execute("SELECT title, category, tags FROM APP_DOCUMENT ORDER BY id DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()

    return rows


def post_doc(request):
    title_list = search_data()
    context = {}

    list_len = int(len(title_list)) + 1
    for i in range(1, list_len):
        context['list' + str(i)] = title_list[i-1]

    return render(request, './app/document_list.html', context)