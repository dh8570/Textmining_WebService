from django.db import migrations, models


class Migration(migrations.Migration):  # 속성 삭제, 수정 DB 정보를 Django project 파일로 이동

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(     # label 필드 삭제
            model_name='document',
            name='label',
        ),
        migrations.RemoveField(     # text 필드 삭제
            model_name='document',
            name='text',
        ),
        migrations.AddField(     # category 필드 추가
            model_name='document',
            name='category',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(     # document 필드 추가
            model_name='document',
            name='document',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(     # title 필드 추가
            model_name='document',
            name='title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(     # tags 필드로 변경
            model_name='document',
            name='tags',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
