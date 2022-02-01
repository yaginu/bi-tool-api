from rest_framework import serializers
from .models import Dataset

import pandas as pd

class DatasetSerializer(serializers.ModelSerializer):

	class Meta:
			model = Dataset
			fields = '__all__'