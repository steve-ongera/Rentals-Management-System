# Generated by Django 5.1.2 on 2024-10-30 20:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rentals', '0012_payment_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='year',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Rentals.payment_year'),
            preserve_default=False,
        ),
    ]
