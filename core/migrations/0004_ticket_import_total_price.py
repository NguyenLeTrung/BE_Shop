# Generated by Django 4.1.4 on 2023-04-16 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_user_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="ticket_import",
            name="total_price",
            field=models.FloatField(null=True),
        ),
    ]
