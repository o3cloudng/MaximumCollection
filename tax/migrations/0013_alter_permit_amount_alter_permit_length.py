# Generated by Django 5.0.4 on 2024-06-16 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tax', '0012_waver_receipt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permit',
            name='amount',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='permit',
            name='length',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
