# Generated by Django 5.0.3 on 2024-03-31 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_phoneproduct_options_phoneproduct_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phoneproduct',
            name='slug',
            field=models.SlugField(max_length=120, unique=True),
        ),
    ]