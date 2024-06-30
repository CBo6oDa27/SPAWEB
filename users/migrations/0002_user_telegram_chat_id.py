# Generated by Django 5.0.6 on 2024-06-30 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="telegram_chat_id",
            field=models.CharField(
                blank=True,
                help_text="Укажите ID чата в телеграм",
                max_length=50,
                null=True,
                verbose_name="id чата в телеграм",
            ),
        ),
    ]
