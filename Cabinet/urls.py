from django.urls import path
from .views import CabinetCreateView, CabinetUpdateView

urlpatterns = [
    path('create/', CabinetCreateView.as_view(), name='cabinet-create'),
    path('update/<int:pk>/', CabinetUpdateView.as_view(), name='cabinet-update'),
]
