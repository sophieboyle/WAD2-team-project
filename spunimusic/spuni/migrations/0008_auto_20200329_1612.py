# Generated by Django 3.0.3 on 2020-03-29 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spuni', '0007_auto_20200319_2024'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='song',
            unique_together={('name', 'artist')},
        ),
    ]
