from django.urls import path, include
from .views import KakaoLoginAPIView, CustomTokenRefreshView
from Users.views import KakaoRedirectView

urlpatterns = [
    path('', KakaoRedirectView.as_view(), name='kakao-code-redirect'),
    path('auth/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('social-login/', include('social_django.urls', namespace='social')),
    path('auth/kakao/', KakaoLoginAPIView.as_view(), name='kakao-login'),
]