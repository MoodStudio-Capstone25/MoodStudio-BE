from django.urls import path
from .views import (
    RecordListView,
    RecordCreateView,
    RecordDetailView,
    RecordUpdateDeleteView,
    RecordImageUploadView,
    ElementListCreateView, 
    ElementDetailView
)

urlpatterns = [
    path('', RecordListView.as_view(), name='record-list'),  
    path('create/', RecordCreateView.as_view(), name='record-create'),
    path('<int:pk>/', RecordDetailView.as_view(), name='record-detail'),
    path('<int:pk>/edit/', RecordUpdateDeleteView.as_view(), name='record-edit-delete'),
    path('upload-images/', RecordImageUploadView.as_view(), name='record-upload-images'),
    path('elements/', ElementListCreateView.as_view(), name='element-list-create'),
    path('elements/<int:pk>/', ElementDetailView.as_view(), name='element-detail'),
]
