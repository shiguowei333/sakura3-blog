from django.db import models
from shortuuidfield import ShortUUIDField
# Create your models here.

class Article(models.Model):
    id = ShortUUIDField(primary_key=True, verbose_name='主键')
    article_content = models.TextField(verbose_name='文章内容')
    article_title = models.CharField(max_length=100, verbose_name='文章标题')
    article_category = models.ForeignKey('category.Category', on_delete=models.PROTECT, verbose_name='文章分类')
    article_tags = models.ManyToManyField('tag.Tag', verbose_name='文章标签')
    visit_count = models.IntegerField(default=0, verbose_name='访问量')
    user = models.ForeignKey('user.User', on_delete=models.PROTECT, verbose_name='作者')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'sakura_article'
        verbose_name = '文章'
        ordering = ['-create_time']
        verbose_name_plural = verbose_name
