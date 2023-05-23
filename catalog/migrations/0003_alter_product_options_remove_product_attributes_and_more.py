# Generated by Django 4.2.1 on 2023-05-23 12:12

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0002_alter_category_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'default_related_name': 'products'},
        ),
        migrations.RemoveField(
            model_name='product',
            name='attributes',
        ),
        migrations.AlterField(
            model_name='product',
            name='bookmarked_by',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(blank=True, to='catalog.category'),
        ),
        migrations.DeleteModel(
            name='Attribute',
        ),
        migrations.DeleteModel(
            name='AttributeGroup',
        ),
    ]
