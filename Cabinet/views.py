from rest_framework import generics, permissions
from .models import Cabinet
from .serializers import CabinetSerializer

class CabinetCreateView(generics.CreateAPIView):
    queryset = Cabinet.objects.all()
    serializer_class = CabinetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CabinetUpdateView(generics.UpdateAPIView):
    queryset = Cabinet.objects.all()
    serializer_class = CabinetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
