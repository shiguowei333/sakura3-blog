from rest_framework import serializers

from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    def get_amount(self, obj):
        return 0
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'amount', 'create_time', 'update_time']