# Generated by Django 5.0.4 on 2024-06-25 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_user_company_logo_alter_user_date_enrolled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_enrolled',
            field=models.DateField(blank=True, null=True),
        ),
    ]
