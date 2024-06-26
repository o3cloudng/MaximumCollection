# Generated by Django 5.0.4 on 2024-06-25 20:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_user_bio_data_user_company_logo_user_country_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='sector',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='sector', to='account.sector'),
            preserve_default=False,
        ),
    ]