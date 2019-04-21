# Generated by Django 2.1.7 on 2019-04-21 00:30

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lock_owners', '0016_auto_20190420_1718'),
    ]

    operations = [
        migrations.CreateModel(
            name='VisitorImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.BinaryField(editable=True, help_text='Image of the user, in bytes')),
                ('filename', models.CharField(help_text='Name of the file to deliver the bytes as', max_length=200)),
                ('name', models.CharField(max_length=100, null=True)),
                ('image_datetime', models.DateTimeField(default=datetime.datetime(2019, 4, 20, 20, 30, 55, 214012), help_text='Date and time the image was captured')),
                ('lock', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='lock_owners.Lock')),
            ],
        ),
        migrations.AlterField(
            model_name='strangerreport',
            name='stranger_report_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 20, 20, 30, 55, 215351), help_text='Date and time the report was made'),
        ),
        migrations.AlterField(
            model_name='tempauth',
            name='auth_code',
            field=models.CharField(default='3754a521-2250-4012-8880-17311947fce2', editable=False, help_text='The temporary authentication code to assign to the user', max_length=200),
        ),
    ]
