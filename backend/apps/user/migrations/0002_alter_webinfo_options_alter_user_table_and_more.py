# Generated by Django 5.1.6 on 2025-03-19 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='webinfo',
            options={'verbose_name': '网站信息表', 'verbose_name_plural': '网站信息表'},
        ),
        migrations.AlterModelTable(
            name='user',
            table='sakura_user',
        ),
        migrations.AlterModelTable(
            name='webinfo',
            table='sakura_web_info',
        ),
    ]
