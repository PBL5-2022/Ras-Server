# Generated by Django 4.0.4 on 2022-05-19 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0003_motor_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupChannel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channelname', models.CharField(max_length=500)),
                ('groupname', models.CharField(max_length=100)),
            ],
        ),
    ]
