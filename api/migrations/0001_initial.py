# Generated by Django 3.1.2 on 2022-01-29 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='データセット名')),
                ('file', models.FileField(upload_to='', verbose_name='ファイル')),
                ('comment', models.TextField(blank=True, max_length=1000, verbose_name='コメント')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
            ],
            options={
                'verbose_name_plural': 'Dataset',
            },
        ),
    ]
