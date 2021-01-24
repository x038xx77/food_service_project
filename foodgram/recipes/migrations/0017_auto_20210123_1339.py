# Generated by Django 3.0.5 on 2021-01-23 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0016_auto_20210122_2204'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='diet',
        ),
        migrations.AddField(
            model_name='recipe',
            name='diets',
            field=models.ManyToManyField(blank=True, related_name='recipe_set', to='recipes.Diet'),
        ),
    ]
