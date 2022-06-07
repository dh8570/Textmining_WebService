import sqlite3
from .parse import class_dic
from django.shortcuts import render


def search_data():
    conn = sqlite3.connect('./db.sqlite3', isolation_level=None)
    cursor = conn.cursor()

    cursor.execute("SELECT title, category, tags FROM APP_DOCUMENT ORDER BY id DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()

    return rows


def progress_data():
    conn = sqlite3.connect('./db.sqlite3', isolation_level=None)
    cursor = conn.cursor()

    cursor.execute('SELECT category FROM APP_DOCUMENT')
    rows = cursor.fetchall()
    conn.close()

    category_amount = {}
    for i, row in enumerate(rows):
        if row[0] not in list(class_dic.values()):
            if '기타' not in list(category_amount.keys()):
                category_amount['기타'] = 1
            else:
                category_amount['기타'] += 1
        rows[i] = row[0]

    for category_value in class_dic.values():
        if rows.count(category_value) != 0:
            category_amount[category_value] = rows.count(category_value)

    progressbar_data = []
    total_amount = len(rows)
    for category, amount in category_amount.items():
        percent = (amount / total_amount) * 100
        data = (category, percent)
        progressbar_data.append(data)

    progressbar_data.sort(key=lambda x: -x[1])
    progressbar_key = []
    progressbar_value = []
    for data in progressbar_data:
        progressbar_key.append(data[0])
        progressbar_value.append(data[1])

    return progressbar_key, progressbar_value


def post_doc(request):
    title_list = search_data()
    context = {}

    list_len = int(len(title_list)) + 1
    for i in range(1, list_len):
        context['list' + str(i)] = title_list[i-1]

    key, value = progress_data()
    category_len = int(len(key))
    context['progressbar_key'] = key
    context['progressbar_value'] = value
    context['progressbar_len'] = category_len

    return render(request, './app/document_list.html', context)