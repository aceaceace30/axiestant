# Generated by Django 4.0.1 on 2022-02-09 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_axie_hidden'),
    ]

    operations = [
        migrations.AddField(
            model_name='axie',
            name='axie_id',
            field=models.PositiveBigIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='axie',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
