# Generated by Django 5.2.3 on 2025-07-11 17:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tutors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('language', models.CharField(max_length=50)),
                ('level', models.CharField(max_length=50)),
                ('schedule_day', models.CharField(max_length=50)),
                ('schedule_start', models.TimeField()),
                ('schedule_end', models.TimeField()),
                ('capacity', models.IntegerField()),
                ('tutor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='tutors.tutor')),
            ],
        ),
    ]
