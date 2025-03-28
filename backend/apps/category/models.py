from django.db import models
from shortuuidfield import ShortUUIDField

# Create your models here.

class Category(models.Model):
    id = ShortUUIDField(primary_key=True, verbose_name='主键')
    category_name = models.CharField(max_length=100)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']
        db_table = 'sakura_category'