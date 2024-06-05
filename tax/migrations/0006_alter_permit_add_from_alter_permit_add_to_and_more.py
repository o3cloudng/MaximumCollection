# Generated by Django 5.0.4 on 2024-06-05 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tax', '0005_waver_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permit',
            name='add_from',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='permit',
            name='add_to',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='permit',
            name='amount',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='permit',
            name='year_installed',
            field=models.DateField(max_length=200, null=True),
        ),
    ]