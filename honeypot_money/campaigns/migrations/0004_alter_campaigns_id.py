# Generated by Django 3.2 on 2021-04-22 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0003_alter_campaigns_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaigns',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
