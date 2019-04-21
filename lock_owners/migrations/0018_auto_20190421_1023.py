# Generated by Django 2.1.7 on 2019-04-21 14:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lock_owners', '0017_auto_20190420_2030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='visitorimage',
            name='lock',
        ),
        migrations.RemoveField(
            model_name='event',
            name='timestamp',
        ),
        migrations.AlterField(
            model_name='strangerreport',
            name='stranger_report_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 21, 10, 23, 9, 434136), help_text='Date and time the report was made'),
        ),
        migrations.AlterField(
            model_name='tempauth',
            name='auth_code',
            field=models.CharField(default='9ce7df9f-b33b-4bcb-9417-393e3d6e2917', editable=False, help_text='The temporary authentication code to assign to the user', max_length=200),
        ),
        migrations.DeleteModel(
            name='VisitorImage',
        ),
    ]
