from django.db import migrations


def populate_blood_compatibility(apps, schema_editor):
    BloodType = apps.get_model('blood', 'BloodType')
    CanDonateTo = apps.get_model('blood', 'CanDonateTo')
    CanReceiveFrom = apps.get_model('blood', 'CanReceiveFrom')

    # Donor blood type: compatible recipient blood types
    compatibility = {
        'O-': ['O-', 'O+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+'],
        'O+': ['O+', 'A+', 'B+', 'AB+'],
        'A-': ['A-', 'A+', 'AB-', 'AB+'],
        'A+': ['A+', 'AB+'],
        'B-': ['B-', 'B+', 'AB-', 'AB+'],
        'B+': ['B+', 'AB+'],
        'AB-': ['AB-', 'AB+'],
        'AB+': ['AB+'],
    }

    blood_types = {
        blood.blood_type: blood
        for blood in BloodType.objects.all()
    }

    for donor_type, recipients in compatibility.items():
        donor = blood_types.get(donor_type)

        if not donor:
            continue

        for recipient_type in recipients:
            recipient = blood_types.get(recipient_type)

            if not recipient:
                continue

            # Donor can donate to recipient
            CanDonateTo.objects.get_or_create(
                blood_type=donor,
                can_donate_to=recipient
            )

            # Recipient can receive from donor
            CanReceiveFrom.objects.get_or_create(
                blood_type=recipient,
                can_receive_from=donor
            )


class Migration(migrations.Migration):

    dependencies = [
        ('blood', '0021_populate_request_reasons'),
    ]

    operations = [
        migrations.RunPython(
            populate_blood_compatibility,
            migrations.RunPython.noop
        ),
    ]