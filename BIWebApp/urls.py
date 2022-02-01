"""BIWebApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from unicodedata import name
from django.contrib import admin
from django.urls import path

from api.views import DatasetListView, DatasetCreateView, DatasetDetailView, DatasetDeleteView, DatasetUpdateView, DatasetPreview, MLModelCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/dataset-list/', DatasetListView.as_view(), name='dataset-list'),
    path('api/dataset-create/', DatasetCreateView.as_view(), name='dataset-create'),
    path('api/dataset-detail/<int:pk>/', DatasetDetailView.as_view(), name='dataset-detail'),
    path('dataset-delete/<int:pk>/', DatasetDeleteView.as_view(), name='detaset-delete'),
    path('dataset-update/<int:pk>/', DatasetUpdateView.as_view(), name='dataset-update'),

    path('api/dataset-preview/<int:pk>/', DatasetPreview.as_view(), name='dataset-preview'),
    path('api/mlmodel-create/<int:pk>/', MLModelCreateView.as_view(), name='mlmodel-create'),
]
