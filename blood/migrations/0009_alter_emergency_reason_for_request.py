# Generated by Django 5.0.6 on 2024-06-24 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blood', '0008_reasonforrequest_alter_emergency_reason_for_request'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emergency',
            name='reason_for_request',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
