# Generated by Django 2.1.7 on 2019-03-24 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lock_owners', '0005_auto_20190324_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitorimage',
            name='image',
            field=models.BinaryField(help_text='Image of the user'),
        ),
    ]