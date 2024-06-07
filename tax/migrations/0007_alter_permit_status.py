# Generated by Django 5.0.4 on 2024-06-06 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tax', '0006_alter_permit_add_from_alter_permit_add_to_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permit',
            name='status',
            field=models.CharField(choices=[('UNPAID', 'Unpaid'), ('PAID', 'Paid'), ('DISPUTED', 'Disputed'), ('Revised', 'Revised')], default='UNPAID', max_length=10),
        ),
    ]
