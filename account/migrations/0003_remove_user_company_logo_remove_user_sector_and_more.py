# Generated by Django 5.0.4 on 2024-05-21 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_user_company_logo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='company_logo',
        ),
        migrations.RemoveField(
            model_name='user',
            name='sector',
        ),
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(default='7 Alakija Street', max_length=300),
            preserve_default=False,
        ),
    ]
