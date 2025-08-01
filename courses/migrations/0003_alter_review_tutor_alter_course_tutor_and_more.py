# Generated by Django 5.2.3 on 2025-07-12 08:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_rename_price_course_price_per_hour_lesson_homework_and_more'),
        ('tutors', '0002_rename_languages_tutor_languages_spoken_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='tutor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutors.tutor'),
        ),
        migrations.AlterField(
            model_name='course',
            name='tutor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tutored_courses', to='tutors.tutor'),
        ),
        migrations.AlterField(
            model_name='student',
            name='favorite_tutors',
            field=models.ManyToManyField(related_name='favorite_students', to='tutors.tutor'),
        ),
        migrations.DeleteModel(
            name='Tutor',
        ),
    ]
