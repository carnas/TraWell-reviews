# Generated by Django 4.1.2 on 2022-11-01 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_first_name_field"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="avg_rate",
            field=models.DecimalField(decimal_places=2, default=2, max_digits=3),
            preserve_default=False,
        ),
    ]