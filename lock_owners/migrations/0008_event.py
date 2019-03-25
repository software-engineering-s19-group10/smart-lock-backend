# Generated by Django 2.1.7 on 2019-03-24 22:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lock_owners', '0007_auto_20190324_2208'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.TimeField(auto_now=True, help_text='Time that the event happened')),
                ('duration', models.IntegerField(help_text='Number of seconds that the event occurred for')),
                ('event_type', models.CharField(help_text='String representing the type of event that occurred', max_length=200)),
                ('lock', models.ForeignKey(help_text='Lock where the event occurred', on_delete=django.db.models.deletion.CASCADE, to='lock_owners.Lock')),
            ],
        ),
    ]