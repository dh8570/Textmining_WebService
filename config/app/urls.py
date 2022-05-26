from django.urls import path
from .views import AppListView, AppCreateView

urlpatterns = [
    # as_view() : 클래스형 뷰를 내부적으로 함수형 뷰로 처리
    # name : 결과 페이지로 보여 줄 템플릿 파일에서 해당 URL을 호출할 때 쓰는 별칭
    path('', AppListView.as_view(), name='list'),    # 주소/app/ 로 이동
    path('write/', AppCreateView.as_view(), name='write'),  # 주소/app/write/ 로 이동
]