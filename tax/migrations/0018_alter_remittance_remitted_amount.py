# Generated by Django 5.0.4 on 2024-06-25 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tax', '0017_remittance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remittance',
            name='remitted_amount',
            field=models.IntegerField(blank=True),
        ),
    ]