# Generated by Django 3.0.5 on 2021-01-22 12:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0010_auto_20210122_0554'),
    ]

    operations = [
        migrations.RenameField(
            model_name='followrecipe',
            old_name='following_recipe',
            new_name='follow_recipe',
        ),
    ]
