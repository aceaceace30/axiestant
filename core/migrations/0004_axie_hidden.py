# Generated by Django 4.0.1 on 2022-02-09 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_axie_ronin'),
    ]

    operations = [
        migrations.AddField(
            model_name='axie',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
    ]
