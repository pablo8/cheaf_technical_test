# Generated by Django 5.1.6 on 2025-02-13 20:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['expiration_date']},
        ),
    ]
