from django.contrib import admin

from .models import Dataset

# Register your models here.
@admin.register(Dataset)
class DatasetAdmint(admin.ModelAdmin):
	list_display = (
		'name',
		'file',
		'comment',
	)