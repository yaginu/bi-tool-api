from random import choices
from django.db import models
from django.conf import settings 

# Create your models here.
class Dataset(models.Model):

	name = models.CharField(verbose_name='データセット名', max_length=40)
	file = models.FileField(verbose_name='ファイル')
	comment = models.TextField(verbose_name='コメント', max_length=1000, blank=True)
	created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

	class Meta:
		verbose_name_plural = 'Dataset'


choices = [
	('Random Forest', 'rdf'),
	('XGBoost', 'xgb'),
	('DNN', 'dnn'),
]

class MLModel(models.Model):

	name = models.CharField(verbose_name='モデル名', max_length=40)
	file = models.FilePathField(path=settings.MEDIA_ROOT, recursive=True, allow_folders=True, verbose_name='ファイルパス')
	comment = models.TextField(verbose_name='コメント', max_length=1000, blank=True)
	created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

	class Meta:
		verbose_name_plural = 'MLModel'