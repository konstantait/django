# Generated by Django 4.2.1 on 2023-06-21 14:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0013_remove_product_bookmarked_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='favorites',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]