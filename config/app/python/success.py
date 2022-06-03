from django.shortcuts import render
import sqlite3


def insert_data(insert_set):
    # connecting DB
    conn = sqlite3.connect('./db.sqlite3', isolation_level=None)
    # connecting cursor
    cursor = conn.cursor()

    cursor.execute("INSERT INTO APP_DOCUMENT(id, title, category, tags, document) VALUES(?, ?, ?, ?, ?)", insert_set)
    conn.close()


def search_data():
    # connecting DB
    conn = sqlite3.connect('./db.sqlite3', isolation_level=None)
    # connecting cursor
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM APP_DOCUMENT")
    rows = cursor.fetchall()
    print(rows)

    conn.close()


def get_data_amount():
    conn = sqlite3.connect('./db.sqlite3', isolation_level=None)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM APP_DOCUMENT")
    rows = cursor.fetchall()
    index = len(rows)

    return index


def get(request):
    title = request.GET.get('title')
    doc = request.GET.get('document')
    category = request.GET.get('category')
    tags = request.GET.get('tags')

    index = get_data_amount()
    insert_set = [index, title, category, tags, doc]

    search_data(insert_set)
    search_data()

    return render(request, './app/document_list.html')
