from django.contrib import admin
from .models import Document

# 정의한 DB 테이블 admin 관리를 위해 선언
admin.site.register(Document)