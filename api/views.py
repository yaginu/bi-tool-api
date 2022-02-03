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
import tensorflow as tf
import xgboost as xgb

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
		data = request.data
		file = Dataset.objects.get(id=kwargs["pk"]).file
		model_dir = os.path.join(settings.MEDIA_ROOT, 'model')
		os.makedirs(model_dir, exist_ok=True)

		df = pd.read_csv(file).drop(['PassengerId', 'Name'] , axis=1)
		y = df.pop('Survived')
		df = df.fillna(df.mean())
		df["Cabin"] = df["Cabin"].fillna(df["Cabin"].mode()[0])
		X = pd.get_dummies(df)
		X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y)

		model_type = data.pop("model_type")
		if model_type == 'rdf':
			clf = RandomForestClassifier()
			clf.fit(X_train, y_train)
			clf.score(X_test, y_test)

			model_path = os.path.join(model_dir, "test_model.pickle")
			with open(model_path, 'wb') as f:
				pickle.dump(clf, f)

		elif model_type == 'xgb':
			d_train = xgb.DMatrix(X_train, y_train)
			param = {'max_depth': 2, 'eta': 1, 'objective': 'binary:logistic'}
			num_round = 10
			bst = xgb.train(param, d_train, num_round)

			model_path = os.path.join(model_dir, "test_model.pickle")
			with open(model_path, 'wb') as f:
				pickle.dump(bst, f)			

		else:
			input_ = tf.keras.layers.Input(shape=X_train.shape[1:])
			hidden = tf.keras.layers.Dense(128, activation="relu")(input_)
			output = tf.keras.layers.Dense(1, activation="sigmoid")(hidden)
			dnn = tf.keras.Model(inputs=[input_], outputs=[output])
			dnn.compile(loss="binary_crossentropy", optimizer="adam")
			dnn.fit(X_train, y_train, epochs=10)
			dnn.evaluate(X_test, y_test)

			model_path = os.path.join(model_dir, "test_model")
			dnn.save(model_path)

		data["file"] = model_path
		serializer = MLModelSerializer(data=data)
		
		if serializer.is_valid(raise_exception=True):
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		
