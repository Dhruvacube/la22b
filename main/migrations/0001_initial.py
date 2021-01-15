# Generated by Django 3.1.5 on 2021-01-15 12:46

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from django.utils.timezone import utc
import main.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Confession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date when this confession was added!')),
                ('confession', models.TextField(verbose_name='Confession')),
            ],
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about_entry', models.TextField(blank=True, null=True, verbose_name='The about us on the entry page')),
                ('title_limit', models.IntegerField(default=5, verbose_name='No of times a one a vote for a particular title  per day')),
                ('nickname_limit', models.IntegerField(default=20, verbose_name='No of times a one a give nicknames per day')),
                ('confession_limit', models.IntegerField(default=2, verbose_name='No of times a one make a confessions day')),
                ('vote_nicknameassigntime_start', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Start Time limit of assigning votes and nickname')),
                ('vote_nicknameassigntime', models.DateTimeField(default=datetime.datetime(2021, 1, 29, 12, 46, 43, 702289, tzinfo=utc), verbose_name='End Time limit of assigning votes and nickname')),
            ],
            options={
                'verbose_name_plural': 'Settings',
            },
        ),
        migrations.CreateModel(
            name='RemoveName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_field', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Time')),
                ('student_models', models.OneToOneField(limit_choices_to=models.Q(hidden=False), on_delete=django.db.models.deletion.DO_NOTHING, to='student.student')),
            ],
            options={
                'verbose_name_plural': 'Remove Name',
                'ordering': ('-time_field',),
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instagram_id', models.CharField(blank=True, max_length=254, null=True, validators=[main.models.validate_insta_id])),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('subject', models.CharField(max_length=100)),
                ('message', models.TextField()),
                ('resolved', models.BooleanField(default=False)),
                ('date_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.ForeignKey(limit_choices_to=models.Q(hidden=False), on_delete=django.db.models.deletion.DO_NOTHING, to='student.student')),
            ],
            options={
                'ordering': ('-date_time',),
            },
        ),
    ]
