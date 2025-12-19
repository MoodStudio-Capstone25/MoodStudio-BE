from rest_framework import serializers
from .models import Record, RecordImage, Element

class RecordImageSerializer(serializers.ModelSerializer):
    image_url = serializers.ImageField(source='image', read_only=True)

    class Meta:
        model = RecordImage
        fields = ['image_url']

class RecordSerializer(serializers.ModelSerializer):
    image_urls = RecordImageSerializer(many=True, read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    date = serializers.DateField(format="%Y-%m-%d", required=False, allow_null=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d", required=False, allow_null=True,)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d", required=False, allow_null=True)
    class Meta:
        model = Record
        fields = [
            'id', 'template', 'category', 'user', 'image_urls',
            'title', 'api_thumbnail', 'rating', 'date',
            'content_title', 'creator', 'cast', 'story',
            'scenes', 'thoughts', 'location', 'companions',
            'created_at', 'updated_at',
        ]

class RecordImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordImage
        fields = ['id', 'record', 'image']

class AngleSerializer(serializers.Serializer):
    x = serializers.FloatField()
    y = serializers.FloatField()
    z = serializers.FloatField()

class PositionSerializer(serializers.Serializer):
    x = serializers.FloatField()
    y = serializers.FloatField()
    z = serializers.FloatField()

class ElementSerializer(serializers.ModelSerializer):
    record = serializers.IntegerField(write_only=True)
    angle = serializers.SerializerMethodField()
    position = serializers.SerializerMethodField()
    category = serializers.CharField(source='record.category', read_only=True)

    class Meta:
        model = Element
        fields = [
            'id', 'record', 'category', 'shape', 'color',
            'angle', 'position', 'size','angle_x',
            'angle_y','angle_z', 'position_x', 'position_y','position_z',
        ]
    
    def create(self, validated_data):
        record_id = validated_data.pop('record')
        try:
            record = Record.objects.get(id=record_id)
        except Record.DoesNotExist:
            raise serializers.ValidationError({"record": "Record with this ID does not exist."})

        element = Element.objects.create(record=record, **validated_data)
        return element
    
    def get_angle(self, obj):
        return {
            'x': obj.angle_x,
            'y': obj.angle_y,
            'z': obj.angle_z,
        }

    def get_position(self, obj):
        return {
            'x': obj.position_x,
            'y': obj.position_y,
            'z': obj.position_z,
        }