# Generated by Django 5.1.8 on 2025-04-28 01:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainmenu', '0003_itemreview_userreview'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userreview',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='userreview',
            name='reviewed_user',
        ),
        migrations.RemoveField(
            model_name='userreview',
            name='reviewer',
        ),
        migrations.DeleteModel(
            name='ItemReview',
        ),
        migrations.DeleteModel(
            name='UserReview',
        ),
    ]
