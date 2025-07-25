from django.db import models
from django.conf import settings

class Cabinet(models.Model):
    #차후를 대비해 한 사람이 여러개의 캐비넷 가질 수 있음
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cabinets')
    color = models.CharField(max_length=50, default='white') #기본 컬러 흰색으로 지정
    position_y = models.IntegerField(default=0) #기본 위치 0으로 지정
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s cabinet ({self.color})"