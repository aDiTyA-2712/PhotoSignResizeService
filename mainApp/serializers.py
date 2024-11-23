from rest_framework import serializers
from .models import ImageUp

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ImageUp
        fields='__all__'
