from django.apps import AppConfig
import pickle
import gzip


classificator = []


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        with gzip.open('./app/model/classificator.pickle', 'rb') as f:
            classification = pickle.load(f)
            classificator.append(classification)
        print(classification)
        pass