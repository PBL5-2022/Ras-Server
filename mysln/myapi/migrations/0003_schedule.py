# Generated by Django 4.0.3 on 2022-03-17 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0002_led_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('device', models.CharField(max_length=60)),
                ('status', models.CharField(max_length=60)),
                ('timesetting', models.CharField(max_length=60)),
            ],
        ),
    ]
