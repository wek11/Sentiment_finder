# Generated by Django 5.0.3 on 2024-06-07 15:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sentiment', '0005_link_text'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Data',
        ),
    ]