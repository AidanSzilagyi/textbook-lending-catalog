# mainmenu/migrations/0006_add_primary_identifier_nullable.py
# Generated by Django 5.1.8 on 2025-04-29 19:15

from django.db import migrations, models
import uuid


def populate_primary_ids(apps, schema_editor):
    """Assign a unique 10-char key to every Item that is still NULL."""
    Item = apps.get_model('mainmenu', 'Item')

    for item in Item.objects.filter(primary_identifier__isnull=True):
        # generate until unique (extremely small collision chance, but safe)
        while True:
            key = uuid.uuid4().hex[:10]
            if not Item.objects.filter(primary_identifier=key).exists():
                item.primary_identifier = key
                item.save(update_fields=['primary_identifier'])
                break


class Migration(migrations.Migration):

    dependencies = [
        ('mainmenu', '0005_itemreview_userreview'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='primary_identifier',
            field=models.CharField(
                max_length=12,
                null=True,
                blank=True,
                editable=False,
            ),
        ),
        migrations.RunPython(populate_primary_ids),
    ]
