from rest_framework import serializers
from .models import Cabinet

class CabinetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cabinet
        fields = ['id', 'user', 'color', 'position_y']
        read_only_fields = ['user']

    def create(self, validated_data):
        cabinet = Cabinet.objects.create(**validated_data)
        return cabinet

    def update(self, instance, validated_data):
        instance.color = validated_data.get('color', instance.color)
        instance.position_y = validated_data.get('position_y', instance.position_y)
        instance.save()
        return instance
