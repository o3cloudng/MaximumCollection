# Generated by Django 5.0.4 on 2024-06-17 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tax', '0014_alter_waver_referenceid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permit',
            name='infra_cost',
            field=models.IntegerField(default=0, max_length=100),
        ),
    ]
