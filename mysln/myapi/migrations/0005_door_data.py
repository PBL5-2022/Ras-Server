# Generated by Django 4.0.4 on 2022-06-12 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0004_groupchannel'),
    ]

    operations = [
        migrations.CreateModel(
            name='Door_Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default='2022-01-01')),
                ('status', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
