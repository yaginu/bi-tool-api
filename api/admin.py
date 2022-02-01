from csv import list_dialects
from django.contrib import admin

from .models import Dataset, MLModel

# Register your models here.
@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
	list_display = (
		'name',
		'file',
		'comment',
	)

@admin.register(MLModel)
class MLModelAdmin(admin.ModelAdmin):
	list_display = (
		'name',
		'file',
		'comment',
	)