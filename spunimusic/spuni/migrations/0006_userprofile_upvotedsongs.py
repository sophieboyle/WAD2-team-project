# Generated by Django 3.0.3 on 2020-03-18 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spuni', '0005_remove_userprofile_upvotedsongs'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='upvotedSongs',
            field=models.ManyToManyField(blank=True, to='spuni.Song'),
        ),
    ]
