# Generated by Django 3.2 on 2021-04-22 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='campaigns',
            old_name='status',
            new_name='active',
        ),
    ]
