# Generated by Django 5.0.3 on 2024-03-31 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_phoneproduct_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='phonecategory',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=120),
        ),
    ]
