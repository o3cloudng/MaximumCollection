# Generated by Django 5.0.4 on 2024-06-08 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='reference',
            new_name='referenceid',
        ),
    ]
