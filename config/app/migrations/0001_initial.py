from django.db import migrations, models


class Migration(migrations.Migration):  # 테이블 생성 DB 정보를 Django project 파일로 이동

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',    # DB 테이블 명
            fields=[    # 해당 테이블 속성
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=1000)),
                ('label', models.CharField(max_length=10)),
                ('tags', models.CharField(max_length=100)),
            ],
        ),
    ]
