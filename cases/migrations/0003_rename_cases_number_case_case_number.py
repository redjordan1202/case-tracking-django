# Generated by Django 4.0.1 on 2022-01-11 05:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0002_rename_cases_case'),
    ]

    operations = [
        migrations.RenameField(
            model_name='case',
            old_name='cases_number',
            new_name='case_number',
        ),
    ]