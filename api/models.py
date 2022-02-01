from django.db import models

# Create your models here.
class Dataset(models.Model):
	"""データセットモデル"""
	name = models.CharField(verbose_name='データセット名', max_length=40)
	file = models.FileField(verbose_name='ファイル')
	comment = models.TextField(verbose_name='コメント', max_length=1000, blank=True)
	created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

	class Meta:
		verbose_name_plural = 'Dataset'