# Generated by Django 3.1.7 on 2021-05-10 13:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_auto_20210422_1614'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'ordering': ['-population']},
        ),
        migrations.AlterUniqueTogether(
            name='city',
            unique_together=set(),
        ),
    ]
