from rest_framework import generics, permissions, serializers
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import Record, RecordImage, Element
from .serializers import RecordSerializer, RecordImageSerializer, ElementSerializer

# 글 작성
class RecordCreateView(generics.CreateAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = [permissions.IsAuthenticated]

# 글 목록 조회
class RecordListView(generics.ListAPIView):
    queryset = Record.objects.all().order_by('-created_at')  # 최신순
    serializer_class = RecordSerializer
    permission_classes = [permissions.IsAuthenticated]


# 글 상세 조회
class RecordDetailView(generics.RetrieveAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = [permissions.IsAuthenticated]

# 글 수정 / 삭제
class RecordUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = [permissions.IsAuthenticated]

# 이미지 업로드 (단일/다중 통합)
class RecordImageUploadView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    class ImageUploadSerializer(serializers.Serializer):
        record = serializers.IntegerField()
        images = serializers.ListField(
            child=serializers.ImageField(),
            allow_empty=False
        )

    def post(self, request, *args, **kwargs):
        serializer = self.ImageUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        record_id = serializer.validated_data['record']
        images = serializer.validated_data['images']

        try:
            record = Record.objects.get(id=record_id, user=request.user)
        except Record.DoesNotExist:
            return Response(
                {'error': '해당 record가 존재하지 않거나 권한이 없습니다.'},
                status=404
            )

        for image in images:
            RecordImage.objects.create(record=record, image=image)

        return Response({
            'status': 'success',
            'message': f'{len(images)}개의 이미지 업로드 완료'
        })

# 전체 요소 조회 + 생성
class ElementListCreateView(generics.ListCreateAPIView):
    queryset = Element.objects.all()
    serializer_class = ElementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        record_id = self.request.query_params.get('record_id')
        if record_id:
            return self.queryset.filter(record_id=record_id)
        return self.queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"elements": serializer.data})

# 단일 요소 조회 + 수정 + 삭제
class ElementDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Element.objects.all()
    serializer_class = ElementSerializer
    permission_classes = [permissions.IsAuthenticated]