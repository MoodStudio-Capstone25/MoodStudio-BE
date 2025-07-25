from django.contrib import admin
from django.urls import path,include
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({'status': 'ok'})

urlpatterns = [
    path('', health_check),  # 루트 주소에 헬스체크 뷰 추가
    path('admin/', admin.site.urls),
    path('users/', include('Users.urls')),
    path('records/', include('Records.urls')),
    path('cabinet/', include('Cabinet.urls')),
 ]
