# Generated by Django 5.2.3 on 2025-07-01 10:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0002_alter_category_options_alter_women_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='women',
            name='cat',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_query_name='posts', to='women.category', verbose_name='Категории'),
        ),
    ]
