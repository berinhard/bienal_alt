# Generated by Django 2.0.6 on 2018-07-21 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actions', '0013_auto_20180721_1423'),
    ]

    operations = [
        migrations.AddField(
            model_name='analyzedimage',
            name='order',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]