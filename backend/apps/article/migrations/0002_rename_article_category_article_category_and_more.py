# Generated by Django 5.1.6 on 2025-04-02 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='article_category',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='article',
            old_name='article_tags',
            new_name='tags',
        ),
    ]
