# Generated by Django 4.1.7 on 2023-03-30 12:36

import core.mixins.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to=core.mixins.models.upload_to)),
                ('status', models.BooleanField(default=True)),
                ('sort_order', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to=core.mixins.models.upload_to)),
                ('status', models.BooleanField(default=True)),
                ('sort_order', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=32)),
                ('code', models.CharField(max_length=5)),
                ('locale', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to=core.mixins.models.upload_to)),
                ('status', models.BooleanField(default=True)),
                ('sort_order', models.IntegerField(default=0)),
                ('model', models.CharField(max_length=64)),
                ('sku', models.CharField(max_length=64)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductDescription',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('tag', models.TextField(blank=True)),
                ('meta_title', models.CharField(max_length=255)),
                ('meta_description', models.CharField(max_length=255)),
                ('meta_keyword', models.CharField(max_length=255)),
                ('language', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='store.language')),
                ('product', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CategoryDescription',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('tag', models.TextField(blank=True)),
                ('meta_title', models.CharField(max_length=255)),
                ('meta_description', models.CharField(max_length=255)),
                ('meta_keyword', models.CharField(max_length=255)),
                ('category', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='store.category')),
                ('language', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='store.language')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
