# Generated by Django 5.0 on 2023-12-06 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list_editor', '0005_affiliations_app_version_card'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='objective_type_id',
            field=models.IntegerField(null=True),
        ),
    ]