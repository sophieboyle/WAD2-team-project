# Generated by Django 3.0.3 on 2020-03-09 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spuni', '0004_auto_20200308_1525'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='upvotedSongs',
        ),
    ]
