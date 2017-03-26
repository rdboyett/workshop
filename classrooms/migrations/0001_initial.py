# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=45)),
                ('code', models.CharField(max_length=10)),
                ('allowJoin', models.BooleanField(default=True)),
                ('classOwnerID', models.IntegerField()),
                ('allUserClass', models.BooleanField(default=False)),
                ('description', models.CharField(max_length=210, null=True, blank=True)),
                ('classDate', models.DateField(null=True, blank=True)),
                ('startTime', models.TimeField(null=True, blank=True)),
                ('endTime', models.TimeField(null=True, blank=True)),
                ('location', models.CharField(max_length=45, null=True, blank=True)),
                ('active', models.BooleanField(default=True)),
                ('classLimit', models.IntegerField(default=30)),
                ('classSize', models.IntegerField(default=0)),
                ('classFull', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['classDate', 'startTime'],
                'verbose_name': 'Session',
                'verbose_name_plural': 'Sessions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClassUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('teacher', models.BooleanField(default=False)),
                ('readOnly', models.BooleanField(default=False)),
                ('avatarBackColor', models.CharField(max_length=45, null=True, blank=True)),
                ('avatarTextColor', models.CharField(max_length=45, null=True, blank=True)),
                ('classrooms', models.ManyToManyField(to='classrooms.Classroom', null=True, blank=True)),
            ],
            options={
                'ordering': ['user__last_name'],
                'verbose_name': 'Session Attendee',
                'verbose_name_plural': 'Session Attendees',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HashTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.CharField(max_length=45)),
                ('timeDate', models.DateTimeField(auto_now=True)),
                ('classroomID', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(max_length=150)),
                ('timeDate', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-timeDate'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='hashtag',
            name='messages',
            field=models.ManyToManyField(to='classrooms.Message', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='classuser',
            name='messages',
            field=models.ManyToManyField(to='classrooms.Message', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='classuser',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='classroom',
            name='messages',
            field=models.ManyToManyField(to='classrooms.Message', null=True, blank=True),
            preserve_default=True,
        ),
    ]
