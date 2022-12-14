# Generated by Django 4.1.2 on 2022-11-06 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_alter_avatar_field"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="email",
            field=models.EmailField(
                default="example@o2.pl", max_length=100, unique=True
            ),
            preserve_default=False,
        ),
    ]
