# Generated by Django 5.0.6 on 2024-09-08 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blood', '0017_alter_emergency_case_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='verification_code',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='verification_code_created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
