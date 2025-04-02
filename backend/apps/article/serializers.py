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
    category_name = serializers.CharField(source='article_category.category_name', read_only=True)
    article_tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, write_only=True)
    tags = TagSerializer(source='article_tags' ,many=True, read_only=True)

    def get_user(self, obj):
        return obj.user.nick_name


    class Meta:
        model = Article
        fields = ['id', 'article_title', 'article_category', 'category_name', 'article_tags', 'tags', 'user', 'create_time', 'update_time']
        extra_kwargs = {
            'article_category': {'write_only': True},
        }


class HandlerArticleSerializer(ArticleSerializer):

    class Meta:
        model = Article
        fields = ['id', 'article_title', 'article_content', 'article_category', 'article_tags']

    def create(self, validated_data):
        user = self.context['request'].user
        tags = validated_data.pop('article_tags')
        article = Article.objects.create(user=user, **validated_data)
        for tag in tags:
            article.article_tags.add(tag)
        article.save()
        return article

    def update(self, instance, validated_data):
        tags = validated_data.pop('article_tags')
        instance.article_tags.set(tags)
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        return instance
