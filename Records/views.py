from rest_framework import generics, permissions, serializers
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from .models import Record, RecordImage, Element
from .serializers import RecordSerializer, RecordImageSerializer, ElementSerializer


# 🚩 글 작성
class RecordCreateView(generics.CreateAPIView):
    """
    RecordSerializer 안에서
    user = HiddenField(CurrentUserDefault())
    로 처리하므로 여기서는 별도 처리 없이 생성만 하면 됨.
    """
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = [permissions.IsAuthenticated]


# 🚩 글 목록 조회 (내 글만)
class RecordListView(generics.ListAPIView):
    serializer_class = RecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 로그인한 사용자 본인의 기록만 조회
        return Record.objects.filter(user=self.request.user).order_by('-created_at')


# 🚩 글 상세 조회 (내 글만)
class RecordDetailView(generics.RetrieveAPIView):
    serializer_class = RecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 다른 사람 글은 pk로 접근해도 404
        return Record.objects.filter(user=self.request.user)


# 🚩 글 수정 / 삭제 (내 글만)
class RecordUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 본인 소유 Record만 수정/삭제 가능
        return Record.objects.filter(user=self.request.user)


# 🚩 이미지 업로드 (단일/다중 통합)
class RecordImageUploadView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    class ImageUploadSerializer(serializers.Serializer):
        record = serializers.IntegerField()
        images = serializers.ListField(
            child=serializers.ImageField(),
            allow_empty=False,
        )

    def post(self, request, *args, **kwargs):
        serializer = self.ImageUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        record_id = serializer.validated_data['record']
        images = serializer.validated_data['images']

        # 여기서도 user 체크를 해서 남의 record에 업로드 못 하게 막음
        try:
            record = Record.objects.get(id=record_id, user=request.user)
        except Record.DoesNotExist:
            return Response(
                {'error': '해당 record가 존재하지 않거나 권한이 없습니다.'},
                status=404,
            )

        for image in images:
            RecordImage.objects.create(record=record, image=image)

        return Response({
            'status': 'success',
            'message': f'{len(images)}개의 이미지 업로드 완료',
        })


# 🚩 전체 요소 조회 + 생성
class ElementListCreateView(generics.ListCreateAPIView):
    serializer_class = ElementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        - 기본적으로는 내 레코드에 속한 Element만
        - ?record_id= 쿼리 파라미터가 있으면 해당 레코드 범위로 한 번 더 필터
        """
        qs = Element.objects.filter(record__user=self.request.user)
        record_id = self.request.query_params.get('record_id')
        if record_id:
            qs = qs.filter(record_id=record_id)
        return qs

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"elements": serializer.data})

    # create()는 ElementSerializer의 로직을 그대로 사용
    # (필요하면 나중에 record가 내 것인지 검증 로직도 추가 가능)


# 🚩 단일 요소 조회 + 수정 + 삭제 (내 레코드의 요소만)
class ElementDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ElementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 내 레코드에 속한 Element만 접근 가능
        return Element.objects.filter(record__user=self.request.user)
