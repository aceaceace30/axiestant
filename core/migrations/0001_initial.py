# Generated by Django 4.0.1 on 2022-01-30 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Axie',
            fields=[
                ('id', models.PositiveBigIntegerField(primary_key=True, serialize=False)),
                ('info', models.JSONField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
