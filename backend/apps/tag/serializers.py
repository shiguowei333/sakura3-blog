from rest_framework import serializers

from .models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['tag_name', 'create_time', 'update_time']
        read_only_fields = ['create_time', 'update_time']