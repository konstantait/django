# Generated by Django 4.2.1 on 2023-05-10 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_alter_user_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_email_valid',
            field=models.BooleanField(default=False),
        ),
    ]
