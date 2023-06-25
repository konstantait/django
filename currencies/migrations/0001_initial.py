# Generated by Django 4.2.2 on 2023-06-25 11:12

import django.core.validators
from django.db import migrations, models
import django_lifecycle.mixins
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Enabled'), (1, 'Disabled')], default=0)),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Added')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='Modified')),
                ('code', models.CharField(max_length=3, unique=True)),
                ('symbol', models.CharField(blank=True, default='', max_length=12)),
                ('rate', models.DecimalField(decimal_places=4, default=1, max_digits=32, validators=[django.core.validators.MinValueValidator(0)])),
            ],
            options={
                'abstract': False,
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
    ]
