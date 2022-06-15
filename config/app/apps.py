from django.apps import AppConfig
import pickle
import gzip


classificator = []  # BERT 모델의 pipeline 모듈을 저장할 리스트


class AppConfig(AppConfig):  # 최적화 작업: 서버 부트 시 BERT 모델 로딩
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        with gzip.open('./app/model/classificator.pickle', 'rb') as f:
            classification = pickle.load(f)
            classificator.append(classification)
        print(classification)
        pass