from django.shortcuts import render
import sqlite3


def get_row(index_id):
    conn = sqlite3.connect('./db.sqlite3', isolation_level=None)
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM APP_DOCUMENT WHERE id = {index_id}")
    post_data = list(cursor.fetchall()[0])
    conn.close()
    return post_data


def search_post_output(request):
    index_id = request.GET.get('id')
    post_data = get_row(index_id)

    context = {
        'title': post_data[3],
        'category': post_data[1],
        'tags': post_data[4],
        'document': post_data[2]
    }

    return render(request, './app/search_post.html', context)