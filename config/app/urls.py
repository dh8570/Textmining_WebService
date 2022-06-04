from django.urls import path
from .views import AppCreateView
from .python.list import post_doc
from .python.parse import get_and_processing
from .python.success import get
from .python.recent_post import recent_post_output
from .python.search import search_processing
from .python.search_post import search_post_output

urlpatterns = [
    # as_view() : 클래스형 뷰를 내부적으로 함수형 뷰로 처리
    # name : 결과 페이지로 보여 줄 템플릿 파일에서 해당 URL을 호출할 때 쓰는 별칭
    path('', post_doc, name='list'),    # 주소/app/ 로 이동
    path('write/', AppCreateView.as_view(), name='write'),  # 주소/app/write/ 로 이동
    path('write/get/', get_and_processing),
    path('success/', get),
    path('recent/post/', recent_post_output),
    path('search/', search_processing),
    path('search/post/', search_post_output),
]