# Generated by Django 5.2.1 on 2025-06-22 20:34

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('balances', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balance',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
