# Generated by Django 4.1.7 on 2023-03-30 13:00

import django.core.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.PositiveIntegerField()),
                ('code', models.CharField(max_length=64)),
                ('status', models.BooleanField(default=True)),
                ('type', models.PositiveSmallIntegerField(choices=[(0, 'cash'), (1, 'percent')], default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=18, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]