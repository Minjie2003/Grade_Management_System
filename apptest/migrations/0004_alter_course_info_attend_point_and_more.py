# Generated by Django 4.2.6 on 2023-12-10 07:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("apptest", "0003_alter_course_info_attend_point_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course_info",
            name="attend_point",
            field=models.TextField(blank=True, default="", null=True),
        ),
        migrations.AlterField(
            model_name="course_info",
            name="exam_point",
            field=models.TextField(blank=True, default="", null=True),
        ),
    ]
