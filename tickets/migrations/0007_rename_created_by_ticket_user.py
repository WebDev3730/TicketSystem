# Generated by Django 5.1.4 on 2025-01-06 19:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0006_rename_user_ticket_created_by'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='created_by',
            new_name='user',
        ),
    ]
