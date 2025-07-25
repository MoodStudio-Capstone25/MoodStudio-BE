import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class KakaoLoginAPIView(APIView):
    def post(self, request):
        kakao_token = request.data.get("access_token")
        if not kakao_token:
            return Response({"error": "No access token provided"}, status=400)

        # Kakao 사용자 정보 요청
        kakao_response = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {kakao_token}"}
        )

        if kakao_response.status_code != 200:
            return Response({"error": "Invalid Kakao token"}, status=400)

        kakao_data = kakao_response.json()
        kakao_id = kakao_data.get("id")
        kakao_account = kakao_data.get("kakao_account", {})
        email = kakao_account.get("email")

        if not email:
            return Response({"error": "카카오 이메일 제공에 동의하지 않았습니다."}, status=400)

        # 유저 생성 또는 조회
        user, created = User.objects.get_or_create(
            username=email,
            defaults={
                "email": email,
                "kakao_id": kakao_id,
                "cabinet_public": True  # ✅ 새 사용자 생성 시 default True
            }
        )

        # 새 유저가 아니라면 kakao_id 누락 시 업데이트
        if not created and not user.kakao_id:
            user.kakao_id = kakao_id
            user.save()

        # JWT 발급
        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "카카오 로그인 성공",
            "tokens": {
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            },
            "user": {
                "email": user.email,
                "cabinet_public": user.cabinet_public  # ✅ 응답에 포함
            }
        })
