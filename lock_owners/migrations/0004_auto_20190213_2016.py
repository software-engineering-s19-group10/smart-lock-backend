# Generated by Django 2.1.7 on 2019-02-13 20:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lock_owners', '0003_auto_20190213_2010'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='owner',
            name='user',
        ),
        migrations.DeleteModel(
            name='Owner',
        ),
    ]
