# Generated by Django 5.1 on 2024-09-07 20:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0002_cat_available'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='cat',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='cats', to=settings.AUTH_USER_MODEL),
        ),
    ]
