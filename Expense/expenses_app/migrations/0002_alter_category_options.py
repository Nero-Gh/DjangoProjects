# Generated by Django 4.1.4 on 2022-12-19 22:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expenses_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
    ]
