# Generated by Django 5.1.4 on 2025-01-15 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0012_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('In Progress', 'In Progress'), ('Resolved', 'Resolved')], default='new', max_length=20),
        ),
    ]
