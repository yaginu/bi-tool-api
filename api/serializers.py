from dataclasses import field
from rest_framework import serializers
from .models import Dataset, MLModel


class DatasetSerializer(serializers.ModelSerializer):

	class Meta:
		model = Dataset
		fields = '__all__'

class MLModelSerializer(serializers.ModelSerializer):

	class Meta:
		model = MLModel
		fields = '__all__'