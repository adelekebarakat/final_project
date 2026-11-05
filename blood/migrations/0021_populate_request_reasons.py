from django.db import migrations


def add_request_reasons(apps, schema_editor):
    ReasonForRequest = apps.get_model('blood', 'ReasonForRequest')

    reasons = [
        'Accident or emergency trauma',
        'Surgery',
        'Childbirth or pregnancy complications',
        'Severe anaemia',
        'Cancer treatment',
        'Medical condition',
        'Other',
    ]

    for reason in reasons:
        ReasonForRequest.objects.get_or_create(reason=reason)


class Migration(migrations.Migration):

    dependencies = [
        ('blood', '0020_populate_blood_types'),
    ]

    operations = [
        migrations.RunPython(
            add_request_reasons,
            migrations.RunPython.noop
        ),
    ]