import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.response import Response
from rest_framework import status
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
            # 인가 코드가 없을 때 앱으로 에러 리다이렉트
            return HttpResponseRedirect("moodstudio://redirect?error=missing_code")

        # 인가 코드가 있을 때 앱으로 코드 전달
        return HttpResponseRedirect(f"moodstudio://redirect?code={code}")
    
class CustomTokenRefreshView(TokenRefreshView):
    """
    refresh_token으로 access_token 재발급 API
    """
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({"error": "Invalid or expired refresh token"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "access": serializer.validated_data["access"],
            "refresh": request.data.get("refresh"),  # 기존 리프레시 유지
            "message": "Access token refreshed successfully"
        })