from django.urls import path
from .views import AppCreateView
from .python.list import post_doc
from .python.parse import get_and_processing
from .python.success import get
from .python.search import search_processing
from .python.search_post import search_post_output
from .python.category_search import category_search_processing

urlpatterns = [
    # as_view() : 클래스형 뷰를 내부적으로 함수형 뷰로 처리
    # name : 결과 페이지로 보여 줄 템플릿 파일에서 해당 URL을 호출할 때 쓰는 별칭
    path('', post_doc, name='list'),    # 주소/app/ 로 이동
    path('write/', AppCreateView.as_view(), name='write'),  # 주소/app/write/ 로 이동
    path('write/get/', get_and_processing),  # 주소/app/write/get/ 로 이동
    path('success/', get),  # 주소/app/success/ 로 이동
    path('search/', search_processing),  # 주소/app/search/ 로 이동
    path('search/post/', search_post_output),   # 주소/app/search/post/ 로 이동
    path('search/category/', category_search_processing),   # 주소/app/search/category/ 로 이동
]