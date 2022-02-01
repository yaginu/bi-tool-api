from django.conf import settings
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
import os
from rest_framework import status

from .models import Dataset
from .serializers import DatasetSerializer, MLModelSerializer

# Create your views here.
class DatasetListView(generics.ListAPIView):
	queryset = Dataset.objects.all()
	serializer_class = DatasetSerializer

class DatasetCreateView(generics.CreateAPIView):
	serializer_class = DatasetSerializer

	# def create(self, request, *args, **kwargs):
		# response = super().create(request)
		# serializer = self.serializer_class('name')
		# print(serializer.data)

		# return Response(status=status.HTTP_201_CREATED)

class DatasetDetailView(generics.RetrieveAPIView):
	queryset = Dataset.objects.all()
	serializer_class = DatasetSerializer

class DatasetDeleteView(generics.DestroyAPIView):
	queryset = Dataset.objects.all()
	serializer_class = DatasetSerializer

class DatasetUpdateView(generics.UpdateAPIView):
	queryset = Dataset.objects.all()
	serializer_class = DatasetSerializer

class DatasetPreview(APIView):
	def get(self, request, *args, **kwargs):
		file = Dataset.objects.get(id=kwargs["pk"]).file
		df = pd.read_csv(file)
		return Response(df.to_json(orient='records'))
	
class MLModelCreateView(APIView):
	def post(self, request, *args, **kwargs):
		file = Dataset.objects.get(id=kwargs["pk"]).file
		df = pd.read_csv(file).drop('PassengerId', axis=1)
		y = df.pop('Survived')
		X = pd.get_dummies(df).fillna(0)
		X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y)
		clf = RandomForestClassifier()
		clf.fit(X_train, y_train)
		# score = clf.score(X_test, y_test)

		model_dir = os.path.join(settings.MEDIA_ROOT, 'model')
		os.makedirs(model_dir, exist_ok=True)
		model_path = os.path.join(model_dir, "test_model.pickle")

		with open(model_path, 'wb') as f:
			pickle.dump(clf, f)

		data = request.data
		data["file"] = model_path
		serializer = MLModelSerializer(data=data)
		
		if serializer.is_valid(raise_exception=True):
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		
