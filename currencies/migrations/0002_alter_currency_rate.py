# Generated by Django 4.2.1 on 2023-06-01 18:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currencies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='rate',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=18, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
