# Generated by Django 2.2.3 on 2019-07-08 15:50

import datetime
from django.db import migrations, models
import django.db.models.deletion
import rapid_responder.models


class Migration(migrations.Migration):

    dependencies = [
        ('rapid_responder', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('time_from', models.TimeField()),
                ('time_to', models.TimeField()),
                ('status', models.CharField(choices=[('red', 'RED'), ('green', 'GREEN'), ('yellow', 'YELLOW')], default=rapid_responder.models.STATUS('green'), max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Responder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=255)),
                ('qualifications', models.ManyToManyField(related_name='responders', to='rapid_responder.Qualification')),
            ],
        ),
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('close_date', models.DateTimeField()),
                ('status', models.CharField(choices=[('unassigned', 'UNASSIGNED'), ('ongoing', 'ONGOING'), ('closed', 'CLOSED'), ('noservice', 'NOSERVICE')], default=rapid_responder.models.CASE_STATUS('unassigned'), max_length=20)),
                ('description', models.TextField(max_length=1000)),
                ('condition', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cases', to='rapid_responder.Condition')),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cases', to='rapid_responder.Patient')),
                ('qualification', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cases', to='rapid_responder.Qualification')),
                ('responder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cases', to='rapid_responder.Responder')),
            ],
        ),
    ]
