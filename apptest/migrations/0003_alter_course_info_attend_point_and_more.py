# Generated by Django 4.2.6 on 2023-12-10 07:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("apptest", "0002_alter_user_user_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course_info",
            name="attend_point",
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="course_info",
            name="exam_point",
            field=models.SmallIntegerField(blank=True, null=True),
        ),
    ]