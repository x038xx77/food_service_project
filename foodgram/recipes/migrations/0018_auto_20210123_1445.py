# Generated by Django 3.0.5 on 2021-01-23 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0017_auto_20210123_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='diets',
            field=models.ManyToManyField(blank=True, related_name='recipe_set', to='recipes.Diet', verbose_name='рацион'),
        ),
    ]
