# Generated by Django 5.0.4 on 2024-06-21 09:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tax', '0016_alter_permit_infra_cost'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Remittance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referenceid', models.CharField(max_length=200)),
                ('remitted_amount', models.IntegerField(default=0)),
                ('receipt', models.FileField(blank=True, null=True, upload_to='uploads/receipts/')),
                ('approved', models.BooleanField(default=False)),
                ('apply_for_waver', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='remit_comp', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
