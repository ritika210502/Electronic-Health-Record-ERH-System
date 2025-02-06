# Generated by Django 4.2.18 on 2025-02-06 09:40

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_doctor_availability_appointment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='contact',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True),
        ),
        migrations.AddIndex(
            model_name='appointment',
            index=models.Index(fields=['doctor', 'date', 'time'], name='api_appoint_doctor__897f4d_idx'),
        ),
    ]
