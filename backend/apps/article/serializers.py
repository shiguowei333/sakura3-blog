from rest_framework import serializers

from .models import Article
from ..category.models import Category
from ..tag.models import Tag


class TagSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    class Meta:
        model = Tag
        fields = ['id', 'tag_name']



class ArticleSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    category_name = serializers.CharField(source='category.category_name', read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, write_only=True)
    tags = TagSerializer(many=True, read_only=True)

    def get_user(self, obj):
        return obj.user.nick_name


    class Meta:
        model = Article
        fields = ['id', 'article_title', 'category', 'category_name', 'tag_ids', 'tags', 'user', 'create_time', 'update_time']
        extra_kwargs = {
            'category': {'write_only': True},
        }


class HandlerArticleSerializer(ArticleSerializer):

    class Meta:
        model = Article
        fields = ['id', 'article_title', 'article_content', 'category', 'tag_ids']

    def create(self, validated_data):
        user = self.context['request'].user
        tags = validated_data.pop('tag_ids')
        article = Article.objects.create(user=user, **validated_data)
        article.tags.set(tags)
        return article

    def update(self, instance, validated_data):
        tags = validated_data.pop('tag_ids')
        instance.tags.set(tags)
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        return instance
