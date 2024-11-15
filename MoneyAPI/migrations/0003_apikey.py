# Generated by Django 5.1.3 on 2024-11-15 19:38

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MoneyAPI', '0002_alter_transaction_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='APIKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('api_key', models.UUIDField(default=uuid.UUID('ff3e6720-09ab-43f8-9ee7-ba3835555a99'), editable=False, unique=True)),
            ],
        ),
    ]
