# Generated by Django 4.1.2 on 2022-11-01 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_alter_avg_rate_field"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="avatar",
            field=models.URLField(blank=True, default=""),
        ),
    ]
