import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponseRedirect
from django.views import View


User = get_user_model()

class KakaoLoginAPIView(APIView):
    def post(self, request):
        kakao_token = request.data.get("access_token")
        if not kakao_token:
            return Response({"error": "No access token provided"}, status=400)

        # 1️⃣ 카카오 사용자 정보 요청
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

        # 2️⃣ kakao_id로 유저 먼저 찾기
        try:
            user = User.objects.get(kakao_id=kakao_id)
        except User.DoesNotExist:
            # 3️⃣ email로 유저 있는지 확인
            user, created = User.objects.get_or_create(
                username=email,
                defaults={
                    "email": email,
                    "cabinet_public": True
                }
            )
            # 4️⃣ kakao_id가 없는 경우에만 저장 (중복 방지)
            if not user.kakao_id:
                user.kakao_id = kakao_id
                user.save()

        # 5️⃣ JWT 발급
        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "카카오 로그인 성공",
            "tokens": {
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            },
            "user": {
                "email": user.email,
                "cabinet_public": user.cabinet_public
            }
        })

class KakaoRedirectView(View):
    def get(self, request):
        code = request.GET.get("code")
        if not code:
            return HttpResponseRedirect("moodstudio://redirect?error=missing_code")
        return HttpResponseRedirect(f"moodstudio://redirect?code={code}")
