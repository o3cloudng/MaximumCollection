# Generated by Django 5.0.4 on 2024-06-16 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tax', '0013_alter_permit_amount_alter_permit_length'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waver',
            name='referenceid',
            field=models.CharField(max_length=200),
        ),
    ]
