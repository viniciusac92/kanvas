# Generated by Django 3.2.6 on 2021-08-06 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kanvas_app', '0005_auto_20210806_1959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='grade',
            field=models.IntegerField(null=True),
        ),
    ]
