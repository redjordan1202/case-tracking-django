# Generated by Django 4.0.1 on 2022-01-15 21:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0007_messages_case_case_creator_case_case_origin_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='case_number',
            field=models.CharField(max_length=6, primary_key=True, serialize=False, validators=[django.core.validators.MinLengthValidator(6)]),
        ),
    ]