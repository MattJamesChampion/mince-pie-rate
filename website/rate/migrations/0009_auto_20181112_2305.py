# Generated by Django 2.1.2 on 2018-11-12 23:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rate', '0008_auto_20181112_2259'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mincepie',
            old_name='box_photo',
            new_name='box_image',
        ),
        migrations.RenameField(
            model_name='mincepie',
            old_name='mince_pie_photo',
            new_name='mince_pie_image',
        ),
    ]
