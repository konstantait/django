# Generated by Django 4.2.1 on 2023-05-10 19:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_lifecycle.mixins
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalog', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Enabled'), (1, 'Disabled')], default=0)),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Added')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='Modified')),
                ('rating', models.PositiveSmallIntegerField(choices=[(0, 'Poor'), (1, 'Fair'), (2, 'Good'), (3, 'Very good'), (4, 'Excellent')], default=4)),
                ('text', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='catalog.product')),
            ],
            options={
                'abstract': False,
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
    ]
