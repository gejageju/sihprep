# Generated by Django 4.0.1 on 2022-08-18 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='uploadedBy',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]