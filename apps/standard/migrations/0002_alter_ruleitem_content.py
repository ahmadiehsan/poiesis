# Generated by Django 3.2.5 on 2021-08-12 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('standard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ruleitem',
            name='content',
            field=models.TextField(verbose_name='content'),
        ),
    ]
