# Generated by Django 2.2.10 on 2021-01-12 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20210112_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='approve',
            field=models.BooleanField(default=False),
        ),
    ]
