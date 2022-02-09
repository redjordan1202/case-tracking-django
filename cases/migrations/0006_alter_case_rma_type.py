# Generated by Django 4.0.1 on 2022-01-12 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0005_alter_case_rma_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='rma_type',
            field=models.CharField(choices=[('Repair', 'Repair'), ('Part', 'Part'), ('Replace', 'Replace')], default='part', max_length=10),
        ),
    ]
