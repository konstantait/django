# Generated by Django 4.2 on 2023-04-24 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_alter_attribute_attribute_group_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribute',
            name='sort_order',
            field=models.IntegerField(default=0, verbose_name='Sort'),
        ),
        migrations.AlterField(
            model_name='attributegroup',
            name='sort_order',
            field=models.IntegerField(default=0, verbose_name='Sort'),
        ),
        migrations.AlterField(
            model_name='category',
            name='sort_order',
            field=models.IntegerField(default=0, verbose_name='Sort'),
        ),
        migrations.AlterField(
            model_name='product',
            name='sku',
            field=models.CharField(max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='sort_order',
            field=models.IntegerField(default=0, verbose_name='Sort'),
        ),
    ]