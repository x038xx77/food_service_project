# Generated by Django 3.0.5 on 2021-01-22 00:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_unit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='ingredients_unit',
        ),
    ]
