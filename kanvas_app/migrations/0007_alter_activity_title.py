# Generated by Django 3.2.6 on 2021-08-09 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kanvas_app', '0006_alter_submission_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='title',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
