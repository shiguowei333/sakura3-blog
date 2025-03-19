from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from shortuuidfield import ShortUUIDField
from django.contrib.auth.hashers import make_password


# Create your models here.

class UserManager(BaseUserManager):
    """
    自定义sakura-admin系统用户模型的manager类
    """
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        初始化用户相关功能
        """
        if not username:
            raise ValueError("必须设置用户名！")

        user = self.model(username=username, **extra_fields)
        user.password = make_password(password)
        user.web_info = WebInfo.objects.create()
        user.save(using=self._db)
        return user


    def create_superuser(self, username, password=None, **extra_fields):
        """
        暂时不增加超级管理员的概念，权限相关暂时使用认证登录即可
        """
        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser):
    """
    重写django默认的用户模型，自定义sakura-admin系统用户模型
    """
    id = ShortUUIDField(primary_key=True, verbose_name='主键')
    username = models.CharField(max_length=128, unique=True, verbose_name='用户名')
    nick_name = models.CharField(max_length=128, blank=True, verbose_name='昵称')
    title = models.CharField(max_length=128, blank=True, verbose_name='头衔')
    avatar = models.CharField(max_length=128, blank=True, verbose_name='头像')
    bg_img = models.CharField(max_length=128, blank=True, verbose_name='背景图')
    github_url = models.CharField(max_length=128, blank=True, verbose_name='github地址')
    web_info = models.ForeignKey('WebInfo', on_delete=models.PROTECT, null=True, blank=True, verbose_name='网站信息')
    is_active = models.BooleanField(default=True, verbose_name='用户状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    objects = UserManager()

    USERNAME_FIELD = "username"

    class Meta:
        verbose_name = "用户表"
        verbose_name_plural = verbose_name
        db_table = 'sakura_user'

class WebInfo(models.Model):
    """
    网站信息表
    """
    id = ShortUUIDField(primary_key=True, verbose_name='主键')
    web_name = models.CharField(max_length=128, blank=True, verbose_name='网站名称')
    header_inform = models.CharField(max_length=128, blank=True, verbose_name='头部通知')
    aside_inform = models.CharField(max_length=128, blank=True, verbose_name='侧面公告')
    web_time = models.DateTimeField(default=timezone.now, null=True, verbose_name='网站创建时间')
    archival_inform = models.CharField(max_length=128, blank=True, verbose_name='备案信息')
    slideshow = models.CharField(max_length=128, blank=True, verbose_name='轮播图')

    class Meta:
        verbose_name = "网站信息表"
        verbose_name_plural = verbose_name
        db_table = 'sakura_web_info'