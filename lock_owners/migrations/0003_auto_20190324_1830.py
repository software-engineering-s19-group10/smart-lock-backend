# Generated by Django 2.1.7 on 2019-03-24 18:30

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lock_owners', '0002_strangerreport'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(help_text='Name of the visitor', max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='permission',
            name='user',
        ),
        migrations.AlterField(
            model_name='strangerreport',
            name='stranger_report_time',
            field=models.DateTimeField(default=datetime.datetime.now, help_text='Date and time the report was made'),
        ),
        migrations.AddField(
            model_name='permission',
            name='visitor',
            field=models.ForeignKey(default=1, help_text='User that permissions are for', on_delete=django.db.models.deletion.CASCADE, to='lock_owners.Visitor'),
            preserve_default=False,
        ),
    ]
