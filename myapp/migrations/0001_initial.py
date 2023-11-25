# Generated by Django 4.2.7 on 2023-11-25 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Student",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                (
                    "department",
                    models.CharField(
                        choices=[("dept1", "Department 1"), ("dept2", "Department 2")],
                        max_length=100,
                    ),
                ),
                ("program", models.CharField(max_length=100)),
                ("graduation_year", models.IntegerField()),
                ("password", models.CharField(max_length=128)),
            ],
        ),
    ]