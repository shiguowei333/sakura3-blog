from rest_framework import serializers

from .models import Article
from ..tag.models import Tag


class TagSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    class Meta:
        model = Tag
        fields = ['id', 'tag_name']

class QueryListArticleSerializer(serializers.ModelSerializer):
    article_tags = TagSerializer(many=True)
    class Meta:
        model = Article
        fields = ['id', 'article_title', 'article_category', 'article_tags', 'user', 'create_time','update_time']


class ArticleSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)
    user = serializers.SerializerMethodField()
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    article_tags = TagSerializer(many=True)

    def get_user(self, obj):
        return obj.user.nick_name

    class Meta:
        model = Article
        fields = ['id', 'article_title', 'article_content', 'article_category', 'article_tags', 'user', 'create_time', 'update_time']

    def create(self, validated_data):
        user = self.context['request'].user
        tags = validated_data.pop('article_tags')
        article = Article.objects.create(user=user, **validated_data)
        for tag in tags:
            article.article_tags.add(tag['id'])
        article.save()
        return article

    def update(self, instance, validated_data):
        tags = validated_data.pop('article_tags')
        instance.article_tags.clear()
        for tag in tags:
            instance.article_tags.add(tag['id'])
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        return instance