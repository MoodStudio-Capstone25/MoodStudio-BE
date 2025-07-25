from django.urls import path, include
from .views import KakaoLoginAPIView

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('social-login/', include('social_django.urls', namespace='social')),
    path('auth/kakao/', KakaoLoginAPIView.as_view(), name='kakao-login'),
]