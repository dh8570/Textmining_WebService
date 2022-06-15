from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Document


class AppListView(ListView):
    # 어떤 모델(테이블)에 대한 제너릭 뷰인지 지정
    model = Document


class AppCreateView(CreateView):
    model = Document
    fields = ['id', 'title', 'category', 'tags', 'document']
    success_url = reverse_lazy('list')
    template_name_suffix = '_create'