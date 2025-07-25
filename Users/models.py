from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    kakao_id = models.CharField(max_length=255, blank=True, null=True)
    cabinet_public = models.BooleanField(default=True)  # 캐비넷 공개 여부, default는 true(공개)상태
