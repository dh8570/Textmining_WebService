import sqlite3
from django.shortcuts import render


def get_row(idx):
    conn = sqlite3.connect('./db.sqlite3', isolation_level=None)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM APP_DOCUMENT ORDER BY id DESC LIMIT 10")
    rows = cursor.fetchall()
    row = list(rows[idx-1])

    return row


def recent_post_output(request):
    idx = request.GET
    idx = int(list(dict(idx).values())[0][0])
    row = get_row(idx)

    context = {
        'title': row[3],
        'document': row[2],
        'category': row[1],
        'tags': row[4]
    }
    return render(request, './app/document_post.html', context)
